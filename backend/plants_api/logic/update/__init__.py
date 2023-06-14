# pylint: disable=too-many-locals, too-many-branches, too-many-statements
"""
Plants update logic is described here.
"""

from collections import defaultdict
from io import BytesIO, StringIO

import pandas as pd
from loguru import logger
from numpy import nan
from sqlalchemy import func, insert, select, update
from sqlalchemy.dialects.postgresql import insert as insert_pg
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import (
    climate_zones,
    cohabitation,
    cohabitation_comments,
    districts,
    genera,
    humidity_types,
    light_types,
    limitation_factors,
    parks,
    plant_types,
    plants,
    plants_climate_zones,
    plants_humidity_types,
    plants_light_types,
    plants_limitation_factors,
    plants_parks,
    plants_soil_acidity_types,
    plants_soil_fertility_types,
    plants_soil_types,
    soil_acidity_types,
    soil_fertility_types,
    soil_types,
)
from plants_api.db.entities.enums import CohabitationType

from .document_parse import (
    get_cohabitation,
    get_plants_from_xlsx_sheets,
    get_plants_genera,
)
from .sheets_configuration import sheets_configuration as s_conf


def normalize(string: str) -> str:
    """
    Normalize plant name to lower-case replacing strange symbols with convenient ones.
    """
    res = string.replace("ё", "е").replace("\xa0", " ").replace("\u0438\u0306", "й").lower().strip()
    while "  " in res:
        res = res.replace("  ", " ")
    return s_conf.plants_naming_exceptions.get(res, res)


s_conf.plants_naming_exceptions = {
    normalize(key): normalize(val) for key, val in s_conf.plants_naming_exceptions.items()
}


async def update_plants_from_xlsx(conn: AsyncConnection, input_xlsx: BytesIO) -> StringIO:
    """
    Parse xlsx with given format and update database entities.
    """
    out = StringIO()
    sheets = pd.read_excel(input_xlsx, sheet_name=None)

    def log(message: str) -> None:
        print(message, file=out)
        logger.info(message)

    log(f"Входной файл имеет {len(sheets)} листов: {' --- '.join(sorted(sheets.keys()))}")

    plants_df = get_plants_from_xlsx_sheets(sheets["Лист13"], sheets["Жизненная форма"])
    genera_df = get_plants_genera(sheets["РодВид"])
    cohabitation_df = get_cohabitation(sheets["Лист23"], genera_df, log)

    comments_ids = {}
    plants_ids = {}
    genera_ids = {}

    plant_types_ids = {}

    type_table_name = {
        "limitation_factors": (
            plants_limitation_factors,
            plants_limitation_factors.c.limitation_factor_id,
            limitation_factors,
        ),
        "soil_acidity_types": (
            plants_soil_acidity_types,
            plants_soil_acidity_types.c.soil_acidity_type_id,
            soil_acidity_types,
        ),
        "soil_fertility_types": (
            plants_soil_fertility_types,
            plants_soil_fertility_types.c.soil_fertility_type_id,
            soil_fertility_types,
        ),
        "soil_types": (
            plants_soil_types,
            plants_soil_types.c.soil_type_id,
            soil_types,
        ),
        "light_types": (
            plants_light_types,
            plants_light_types.c.light_type_id,
            light_types,
        ),
        "humidity_types": (
            plants_humidity_types,
            plants_humidity_types.c.humidity_type_id,
            humidity_types,
        ),
    }

    # считывание парков

    # district:
    #   - park:
    #       - plant
    #       - plant
    plants_locations: dict[str, dict[str, list[str]]] = defaultdict(lambda: {})
    for district_sheet_name in s_conf.park_sheets:
        if (parks_plants := sheets.get(district_sheet_name)) is None:
            log(f"Лист с парками '{district_sheet_name}' не найден в документе, попускается!")
            continue
        for park_name in parks_plants.columns:
            park_plants = list(parks_plants[park_name].dropna().apply(normalize).unique())
            plants_locations[district_sheet_name][park_name] = park_plants

    # Загрузка жизненных форм с соответствующего листа.
    statement = select(plant_types.c.name, plant_types.c.id)
    for name, idx in await conn.execute(statement):
        plant_types_ids[name] = idx

    insert_statement = insert(plant_types).returning(plant_types.c.id)
    for name in plants_df["Тип растения"].unique():
        if name is None or name != name or name in plant_types_ids:  # pylint: disable=comparison-with-itself
            continue
        plant_types_ids[name] = (await conn.execute(insert_statement, {"name": name})).scalar()

    # Загрузка родов
    insert_statement = insert(genera).returning(genera.c.id)
    for name in set(genera_df["Род"]):
        statement = select(genera.c.id).where(func.lower(genera.c.name_ru) == name.lower())
        if (res := (await conn.execute(statement)).fetchone()) is None:
            res = (await conn.execute(insert_statement, {"name_ru": name})).fetchone()
        genera_ids[name.lower()] = res[0]

    # Загрузка комментрариев сочетаемости с листа
    insert_statement = insert(cohabitation_comments).returning(cohabitation_comments.c.id)
    for comment in [
        c for c in cohabitation_df["Краткий комментарий"].unique() if c == c  # pylint: disable=comparison-with-itself
    ]:
        statement = select(cohabitation_comments).where(cohabitation_comments.c.text == comment)
        if (res := (await conn.execute(statement)).fetchone()) is None:
            res = (await conn.execute(insert_statement, {"text": comment})).fetchone()
        comments_ids[comment] = res[0]

    # Синхронизация названия на русском по названию на латыни.
    log("Обновление названий на русском языке в соответствии с документом")
    was_updated = 0
    for _, (name_ru, name_lat) in plants_df[["Название", "Латинское название"]].iterrows():
        statement = select(plants.c.name_ru).where(plants.c.name_latin == name_lat)
        if (res := (await conn.execute(statement)).fetchone()) is not None:
            if res[0] != name_ru:
                log(f"Обновление названия по-русски: {res[0]} -> {name_ru} (название на латыни: {name_lat})")
                statement = update(plants).where(plants.c.name_latin == name_lat).values(name_ru=name_ru)
                await conn.execute(statement)
                was_updated += 1
    if was_updated == 0:
        log("Названия на русском языке соответствуют тем, что указаны в документе.")

    statement = select(climate_zones.c.usda_number, climate_zones.c.id)
    usda_numbers_climate_zones = dict((await conn.execute(statement)).fetchall())

    # Загрузка и обновление растений
    inserted_new = 0
    inserted_factors = 0
    updated_factors = 0

    for idx, line in plants_df.replace({nan: None}).iterrows():
        statement = select(plants.c.id).where(plants.c.name_ru == line["Название"])
        if (res := (await conn.execute(statement)).fetchone()) is None:
            insert_statement = insert(plants).returning(plants.c.id)
            res = (
                await conn.execute(
                    insert_statement,
                    {
                        "name_ru": line["Название"],
                        "name_latin": line["Латинское название"],
                        "genus_id": (
                            genera_ids.get(
                                genera_df[genera_df["Вид"].apply(normalize) == normalize(line["Название"])]["Род"]
                                .iloc[0]
                                .lower()
                            )
                            if normalize(line["Название"]) in genera_df["Вид"].apply(normalize)
                            else None
                        ),
                        "height_avg": line["Высота"],
                        "crown_diameter": line["Размер кроны"],
                        "spread_aggressiveness_level": line["Агрессивность развития"],
                        "survivability_level": line["Живучесть"],
                        "is_invasive": bool(line["Инвазивный вид"]),
                    },
                )
            ).fetchone()
            inserted_new += 1
        plant_id = res[0]
        insert_statement = insert(plants_climate_zones)
        for name, value in line.items():
            if (name not in s_conf.additional_columns) and (
                name not in s_conf.plants_columns_mapping or (value := str(value).strip()) not in ("-1", "0", "1")
            ):
                continue
            if name.startswith("USDA"):
                value = (
                    CohabitationType.positive
                    if value == "1"
                    else CohabitationType.neutral
                    if value == "0"
                    else CohabitationType.negative
                )
                usda_number = int(name[len("USDA") :])
                statement = select(plants_climate_zones.c.type).where(
                    (plants_climate_zones.c.plant_id == plant_id)
                    & (plants_climate_zones.c.climate_zone_id == usda_numbers_climate_zones[usda_number])
                )
                if (res := (await conn.execute(statement)).fetchone()) is None:
                    await conn.execute(
                        insert_statement,
                        {
                            "plant_id": plant_id,
                            "climate_zone_id": usda_numbers_climate_zones[usda_number],
                            "type": value,
                        },
                    )
                    inserted_factors += 1
                elif res[0] != value:
                    statement = (
                        update(plants_climate_zones)
                        .values(type=value)
                        .where(
                            plants_climate_zones.c.plant_id == plant_id,
                            plants_climate_zones.c.climate_zone_id == usda_numbers_climate_zones[usda_number],
                        )
                    )
                    await conn.execute(statement)
                    updated_factors += 1
                continue
            if name == "Тип растения":
                statement = select(plants.c.type_id).where(plants.c.id == plant_id)
                if (await conn.execute(statement)).scalar() != value:
                    statement = update(plants).where(plants.c.id == plant_id).values(type_id=plant_types_ids[value])
                    await conn.execute(statement)
                continue
            try:
                value = (
                    CohabitationType.positive
                    if value == "1"
                    else CohabitationType.neutral
                    if value == "0"
                    else CohabitationType.negative
                )
                plants_to_table, table_column, table_types = type_table_name[s_conf.plants_columns_mapping[name]]
                statement = select(plants_to_table.c.type).where(
                    (plants_to_table.c.plant_id == plant_id)
                    & (table_column == select(table_types.c.id).where(table_types.c.name == name).scalar_subquery())
                )
                if (res := (await conn.execute(statement)).fetchone()) is None:
                    statement = insert(plants_to_table).values(
                        plant_id=plant_id,
                        type=value,
                        **{
                            table_column.name: select(table_types.c.id)
                            .where(table_types.c.name == name)
                            .scalar_subquery()
                        },
                    )
                    await conn.execute(statement)
                    inserted_factors += 1
                elif res[0] != value:
                    statement = (
                        update(plants_to_table)
                        .where(
                            (plants_to_table.c.plant_id == plant_id)
                            & (
                                table_column
                                == select(table_types.c.id).where(table_types.c.name == name).scalar_subquery()
                            )
                        )
                        .values(type=value)
                    )
                    await conn.execute(statement)
                    updated_factors += 1
            except Exception as exc:
                log(repr(exc))
                raise
    log(f"Добавлено растений {inserted_new}")
    log(f"Добавлено свойств: {inserted_factors}")
    log(f"Обновлено свойств: {updated_factors}")
    log("")

    # Обновление родов
    statement = select(plants.c.name_ru, plants.c.id)
    plants_ids = {normalize(name): idx for name, idx in await conn.execute(statement)}
    statement = select(plants.c.id, plants.c.genus_id).where(
        plants.c.genus_id != None  # pylint: disable=singleton-comparison
    )
    plants_genera = dict((await conn.execute(statement)).fetchall())
    updated_genera = 0
    for name in set(genera_df["Вид"]):
        if normalize(name) not in plants_ids:
            name = f"'{name}'"
            log(f"Растение {name:<40} отсутствует в базе данных, хотя указано его соовтетствие роду.")
    for _, (genus_name, plant_name) in genera_df[["Род", "Вид"]].iterrows():
        if (plant_name := normalize(plant_name)) in plants_ids:
            genus_name = genus_name.lower()
            if plants_genera.get(plants_ids[plant_name]) != genera_ids[genus_name]:
                statement = (
                    update(plants).where(plants.c.id == plants_ids[plant_name]).values(genus_id=genera_ids[genus_name])
                )
                await conn.execute(statement)
                updated_genera += 1
                plants_genera[plants_ids[plant_name]] = genera_ids[genus_name]
    if updated_genera != 0:
        log(f"Updated {updated_genera} plants genera")

    # Вставка сочетаемостей
    inserted_straight = 0
    inserted_back = 0
    updated = 0
    missing_genera = (
        set(cohabitation_df["Род"].apply(str.lower)) | set(cohabitation_df["Род.1"].apply(str.lower))
    ) - set(genera_df["Род"].apply(str.lower))
    insert_statement = insert(cohabitation)
    for _, (genus_1, value, genus_2, comment) in cohabitation_df[
        ["Род", "Совместимость", "Род.1", "Краткий комментарий"]
    ].iterrows():
        genus_1, genus_2 = genus_1.lower(), genus_2.lower()
        if genus_1 in missing_genera or genus_2 in missing_genera:
            continue
        statement = select(cohabitation.c.cohabitation_type).where(
            (cohabitation.c.genus_id_1 == genera_ids[genus_1]) & (cohabitation.c.genus_id_2 == genera_ids[genus_2])
        )
        if (res := (await conn.execute(statement)).fetchone()) is not None:
            value_now = 1 if res[0] == CohabitationType.positive else 0 if res[0] == CohabitationType.neutral else -1
            if value_now != value:
                statement = (
                    update(cohabitation)
                    .where(
                        (cohabitation.c.genus_id_1 == genera_ids[genus_1])
                        & (cohabitation.c.genus_id_2 == genera_ids[genus_2])
                    )
                    .values(
                        cohabitation_type=(
                            CohabitationType.positive
                            if value == 1
                            else CohabitationType.neutral
                            if value == 0
                            else CohabitationType.negative
                        )
                    )
                )
                await conn.execute(statement)
                updated += 1
        else:
            await conn.execute(
                insert_statement,
                {
                    "genus_id_1": genera_ids[genus_1],
                    "genus_id_2": genera_ids[genus_2],
                    "cohabitation_type": CohabitationType.positive
                    if value == 1
                    else CohabitationType.neutral
                    if value == 0
                    else CohabitationType.negative,
                    "comment_id": comments_ids[comment] if comment in comments_ids else None,
                },
            )
            inserted_straight += 1

    for _, (genus_1, value, genus_2, comment) in cohabitation_df[
        ["Род", "Совместимость", "Род.1", "Краткий комментарий"]
    ].iterrows():
        genus_1, genus_2 = genus_1.lower(), genus_2.lower()
        if genus_1 in missing_genera or genus_2 in missing_genera:
            continue
        statement = select(cohabitation.c.cohabitation_type).where(
            (cohabitation.c.genus_id_1 == genera_ids[genus_2]) & (cohabitation.c.genus_id_2 == genera_ids[genus_1])
        )
        if (res := (await conn.execute(statement)).fetchone()) is not None:
            value_now = 1 if res[0] == CohabitationType.positive else 0 if res[0] == CohabitationType.neutral else -1
            if value_now != value:
                log(
                    f"Сочетаемость родов {genus_2:<20} и {genus_1:<20} имеет значение "
                    f" {value_now} напрямую и {value} в обратную сторону"
                )
        else:
            await conn.execute(
                insert_statement,
                {
                    "genus_id_1": genera_ids[genus_2],
                    "genus_id_2": genera_ids[genus_1],
                    "cohabitation_type": CohabitationType.positive
                    if value == 1
                    else CohabitationType.neutral
                    if value == 0
                    else CohabitationType.negative,
                    "comment_id": comments_ids[comment] if comment in comments_ids else None,
                },
            )
            inserted_back += 1
    log(
        f"Добавлено {inserted_straight} прямых значений совместимости + {inserted_back}"
        f" обратных значений. Обновлены {updated} связей."
    )
    log("")

    missing_plants = set()
    for district_name, parks_dict in plants_locations.items():
        statement = select(districts.c.id).where(districts.c.sheet_name == district_name)
        if (res := (await conn.execute(statement)).fetchone()) is None:
            statement = insert(districts).values(name=district_name, sheet_name=district_name).returning(districts.c.id)
            res = (await conn.execute(statement)).fetchone()
        district_id = res[0]

        for park_name, park_plants in parks_dict.items():
            statement = select(parks.c.id).where((parks.c.district_id == district_id) & (parks.c.name == park_name))
            if (res := (await conn.execute(statement)).fetchone()) is None:
                statement = insert(parks).values(district_id=district_id, name=park_name).returning(parks.c.id)
                res = (await conn.execute(statement)).fetchone()
            park_id = res[0]
            for plant_name in park_plants:
                if plant_name not in plants_ids:
                    log(
                        f"Растение '{plant_name}' из парка '{park_name}' в районе"
                        f" '{district_name}' не найдено в базе данных, пропускается!"
                    )
                    missing_plants.add(plant_name)
                    continue
                statement = (
                    insert_pg(plants_parks)
                    .values(plant_id=plants_ids[plant_name], park_id=park_id)
                    .on_conflict_do_nothing(index_elements=["plant_id", "park_id"])
                )
                await conn.execute(statement)
    if len(missing_plants) > 0:
        log(f"{len(missing_plants)} отсутствующие в БД растения, указанные в парках: {', '.join(missing_plants)}")

    await conn.commit()
    return out


__all__ = [
    "update_plants_from_xlsx",
]
