import os
import sys
from datetime import date

import pandas as pd
import psycopg2
from numpy import nan
from tqdm import tqdm

filename = "База данных породного состава.xlsx"
if len(sys.argv) > 1:
    filename = sys.argv[1]
if filename != "--help" and not os.path.isfile(filename):
    print(f"Файл {filename} не найден")
    filename = "--help"
if filename == "--help":
    print("Скрипт для загрузки xlsx документа с информацией о растениях с заданным форматом в базу данных")
    print(f"Использование: python {sys.argv[0]} <путь/до/файла.xlsx>")
    print("Используемые переменные окружения: DB_HOST,DB_PORT,DB_NAME,DB_USER,DB_PASS")

db_host = os.environ.get("DB_HOST", "localhost")
db_port = os.environ.get("DB_PORT", 5432)
db_name = os.environ.get("DB_NAME", "greendb")
db_user = os.environ.get("DB_USER", "postgres")
db_pass = os.environ.get("DB_PASS", "postgres")

# Известные переименования и функция нормализации названий для сравнения

exc = {"Клен сахаристый": "Клён сахарный"}


def normalize(s: str) -> str:
    res = s.replace("ё", "е").replace("\xa0", " ").replace("\u0438\u0306", "й").lower().strip()
    return exc[res] if res in exc else res


exc = {normalize(key): normalize(val) for key, val in exc.items()}

# Начало работы

print(f"В качестве входного файла информации о растениях используется {filename}")
print(f"Подключение к базе данных будет произведено как postgresql://{db_user}@{db_host}:{db_port}/{db_name}")
print()

get_conn = lambda: psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_pass,
    application_name="update_plants",
    connect_timeout=10,
)

sheets = pd.read_excel(filename, sheet_name=None)
print(f"Входной файл имеет {len(sheets)} листов: {' --- '.join(sorted(sheets.keys()))}")
print()

names_mapping = {
    "Уст. к пересыханию": "Устойчивость к пересыханию",
    "Уст. к подтоплению": "Устойчивость к подтоплению",
    "Агресс-ть развития": "Агрессивность развития",
    "Назначение, хар-р использ-я": "Назначение, характер использования",
    "Ксерофит": "Мало воды",
    "Мезофит": "Средняя",
    "Гигрофит": "Много воды",
    "Средне плодородные": "Средне плодородная",
    "Бедные почвы": "Бедная почва",
}

# Объединение полей, относящихся к одной таблице
types_mapping = {}
for name in (
    "Устойчивость к переуплотнению",
    "Устойчивость к засолению",
    "Устойчивость к пересыханию",
    "Устойчивость к подтоплению",
    "Газостойкость",
    "Ветроустойчивость",
):
    types_mapping[name] = "limitation_factors"

for name in (
    "Сильнокислые (4)",
    "Кислые (5)",
    "Слабокислые (6)",
    "Нейтральные (7)",
    "Слабощелочные (8)",
    "Щелочные (9)",
    "Сильнощелочные (10)",
):
    types_mapping[name] = "soil_acidity_types"

for name in ("Плодородная", "Средне плодородные", "Бедные почвы"):
    types_mapping[name] = "soil_fertility_types"

for name in (
    "Песчаная",
    "Супесчаная",
    "Суглинистая",
    "Глинистая",
    "Каменистые",
    "Щебнистые",
    "Тяжёлая",
    "Хорошо дренированная",
):
    types_mapping[name] = "soil_types"

for name in ("Полное освещение", "Полутень", "Тень"):
    types_mapping[name] = "light_types"

for name in ("Мало воды", "Средняя", "Много воды"):
    types_mapping[name] = "humidity_types"

# Дополнительные поля, обрабатываемые при загрузке
additional_mapping = {"Тип растения", *(f"USDA{i}" for i in range(1, 12))}

# Считывание страницы растений

plants = sheets["Лист13"].copy()

plants.iat[1, 0] = "idx"
plants.iat[1, 1] = "Название"
plants.iat[1, 2] = "Латинское название"
plants.at[1, "Высота"] = "Высота"
plants.at[1, "Размер кроны"] = "Размер кроны"
plants.at[1, "Жизненная форма"] = "Жизненная форма"
plants.at[1, "Агресс-ть развития"] = "Агресс-ть развития"
plants.at[1, "Живучесть"] = "Живучесть"
plants.at[1, "Инвазивный вид"] = "Инвазивный вид"
plants.at[1, "Период цветения"] = "Период цветения"
plants.at[1, "Назначение, хар-р использ-я"] = "Назначение, хар-р использ-я"
plants.columns = plants.iloc[1]
plants = plants.rename(names_mapping, axis=1).set_index("idx").iloc[3:]
plants["Высота"] = plants["Высота"].apply(
    lambda x: None
    if x == "-"
    else float(x[x.index("-") + 1 :])
    if isinstance(x, str) and "-" in x
    else float(x)
    if isinstance(x, str)
    else float(f"{x.day}.{x.month}" if isinstance(x, date) else x)
)
plants["Размер кроны"] = plants["Размер кроны"].apply(
    lambda x: None
    if x == "-"
    else float(x)
    if isinstance(x, str)
    else float(f"{x.day}.{x.month}" if isinstance(x, date) else x)
)
plants = plants.dropna(subset="Латинское название").drop_duplicates(subset="Латинское название")

# Считывание жизненных форм

lf = sheets["Жизненная форма"]
lf["Сокращение"] = lf["Сокращение"].apply(str.lower)
lf = lf.rename({"Расшифровка": "Тип растения"}, axis=1)
plant_types = pd.Series(lf.set_index("Сокращение")["Тип растения"])
plants = plants.merge(plant_types, left_on="Жизненная форма", right_index=True)

# Считывание родов
cohabitation, genera = sheets["Лист23"], sheets["РодВид"][["Род", "Вид"]].dropna()
comments = [c for c in cohabitation["Краткий комментарий"].unique() if c == c]
missing_genera = (set(cohabitation["Род"].apply(str.lower)) | set(cohabitation["Род.1"].apply(str.lower))) - set(
    genera["Род"].apply(str.lower)
)
print("Отсутствующие рода, указанные в сочетаемости родов:", ", ".join(missing_genera))

print(
    f"Указаны {cohabitation.shape[0]} сочетаемостей родов, {cohabitation.drop_duplicates(['Род', 'Род.1']).shape[0]} после удаления дубликатов"
)
cohabitation = cohabitation.drop_duplicates(["Род", "Род.1"]).dropna(subset=["Род", "Род.1"])

comments_ids = {}
plants_ids = {}
genera_ids = {}

plant_types_ids = {}

type_table_name = {
    "limitation_factors": ("plants_limitation_factors", "limitation_factor_id", "limitation_factors"),
    "soil_acidity_types": ("plants_soil_acidity_types", "soil_acidity_type_id", "soil_acidity_types"),
    "soil_fertility_types": ("plants_soil_fertility_types", "soil_fertility_type_id", "soil_fertility_types"),
    "soil_types": ("plants_soil_types", "soil_type_id", "soil_types"),
    "light_types": ("plants_light_types", "light_type_id", "light_types"),
    "humidity_types": ("plants_humidity_types", "humidity_type_id", "humidity_types"),
}
try:
    with get_conn() as conn, conn.cursor() as cur:

        # Загрузка жизненных форм с соответствующего листа.
        cur.execute("SELECT name, id FROM plant_types")
        for name, idx in cur.fetchall():
            plant_types_ids[name] = idx
        for name in plant_types:
            if name in plant_types_ids:
                continue
            cur.execute("INSERT INTO plant_types (name) VALUES (%s) RETURNING id", (name,))
            plant_types_ids[name] = cur.fetchone()

        # Загрузка родов
        for name in set(genera["Род"]):
            cur.execute("SELECT id FROM genera WHERE lower(name_ru) = %s", (name.lower(),))
            if (res := cur.fetchone()) is None:
                cur.execute("INSERT INTO genera (name_ru) VALUES (%s) RETURNING id", (name,))
                res = cur.fetchone()
            genera_ids[name.lower()] = res[0]

        # Загрузка комментрариев сочетаемости с листа
        for comment in comments:
            cur.execute("SELECT id FROM cohabitation_comments WHERE text = %s", (comment,))
            if (res := cur.fetchone()) is None:
                cur.execute("INSERT INTO cohabitation_comments (text) VALUES (%s) RETURNING id", (comment,))
                res = cur.fetchone()
            comments_ids[comment] = res[0]

        # Синхронизация названия на русском по названию на латыни.
        print("Обновление названий на русском языке в соответствии с документом")
        was_updated = 0
        for _, (name_ru, name_lat) in plants[["Название", "Латинское название"]].iterrows():
            cur.execute("SELECT name_ru FROM plants WHERE name_latin = %s", (name_lat,))
            if (res := cur.fetchone()) is not None:
                if res[0] != name_ru:
                    print(f"Обновление названия по-русски: {res[0]} -> {name_ru} (название на латыни: {name_lat})")
                    cur.execute("UPDATE plants SET name_ru = %s WHERE name_latin = %s", (name_ru, name_lat))
                    was_updated += 1
        if was_updated != 0:
            if input("Зафиксировать изменения в количестве {was_updated} (выход в случае отмены)? ").lower() not in (
                "y",
                "1",
                "д",
            ):
                conn.rollback()
                print("Изменения обращены.")
                exit(1)
            else:
                conn.commit()
                print("Изменения зафиксированы в базе данных.")
        else:
            print("Названия на русском языке соответствуют тем, что указаны в документе.")

        # Загрузка и обновление растений
        inserted_new = 0
        inserted_factors = 0
        updated_factors = 0

        for idx, line in tqdm(
            plants.replace({nan: None}).iterrows(), total=plants.shape[0], desc="Загрукза и обновление растений"
        ):
            cur.execute("SELECT id FROM plants WHERE name_ru = %s", (line["Название"],))
            if (res := cur.fetchone()) is None:
                cur.execute(
                    "INSERT INTO plants (name_ru, name_latin, genus_id, height_avg, crown_diameter, spread_aggressiveness_level, survivability_level, is_invasive)"
                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id",
                    (
                        line["Название"],
                        line["Латинское название"],
                        (
                            genera_ids.get(
                                genera[genera["Вид"].apply(normalize) == normalize(line["Название"])]["Род"]
                                .iloc[0]
                                .lower()
                            )
                            if normalize(line["Название"]) in genera["Вид"].apply(normalize)
                            else None
                        ),
                        line["Высота"],
                        line["Размер кроны"],
                        line["Агрессивность развития"],
                        line["Живучесть"],
                        bool(line["Инвазивный вид"]),
                    ),
                )
                res = cur.fetchone()
                inserted_new += 1
            plant_id = res[0]
            for name, value in line.items():
                if (name not in additional_mapping) and (
                    name not in types_mapping or (value := str(value).strip()) not in ("0", "1")
                ):
                    continue
                if name.startswith("USDA"):
                    value = value == "1"
                    usda_number = int(name[len("USDA") :])
                    cur.execute(
                        "SELECT is_stable FROM plants_climate_zones"
                        " WHERE plant_id = %s AND climate_zone_id = (SELECT id FROM climate_zones WHERE usda_number = %s)",
                        (plant_id, usda_number),
                    )
                    if (res := cur.fetchone()) is None:
                        cur.execute(
                            "INSERT INTO plants_climate_zones (plant_id, climate_zone_id, is_stable)"
                            " VALUES (%s, (SELECT id FROM climate_zones WHERE usda_number = %s), %s)",
                            (plant_id, usda_number, value),
                        )
                        inserted_factors += 1
                    elif res[0] != bool(int(value)):
                        cur.execute(
                            "UPDATE plants_climate_zones SET is_stable = %s"
                            " WHERE plant_id = %s AND climate_zone_id = (SELECT id FROM climate_zones WHERE usda_number = %s)",
                            (value, plant_id, usda_number),
                        )
                        updated_factors += 1
                    continue
                elif name == "Тип растения":
                    cur.execute("SELECT type_id FROM plants WHERE id = %s", (plant_id,))
                    if cur.fetchone()[0] != value:
                        cur.execute(
                            "UPDATE plants SET type_id = %s WHERE id = %s",
                            (plant_types_ids[value], plant_id),
                        )
                    continue
                try:
                    table_values = type_table_name[types_mapping[name]]
                    cur.execute(
                        f"SELECT is_stable FROM {table_values[0]}"
                        f" WHERE plant_id = %s AND {table_values[1]} = (SELECT id FROM {table_values[2]} WHERE name = %s)",
                        (plant_id, name),
                    )
                    if (res := cur.fetchone()) is None:
                        cur.execute(
                            f"INSERT INTO {table_values[0]} (plant_id, {table_values[1]}, is_stable)"
                            f" VALUES (%s, (SELECT id FROM {table_values[2]} WHERE name = %s), %s)",
                            (plant_id, name, value),
                        )
                        inserted_factors += 1
                    elif res[0] != value:
                        cur.execute(
                            f"UPDATE {table_values[0]} SET is_stable = %s"
                            f" WHERE plant_id = %s AND {table_values[1]} = (SELECT id FROM {table_values[2]} WHERE name = %s)",
                            (value, plant_id, name),
                        )
                        updated_factors += 1
                except Exception:
                    print(f"{types_mapping[name]} - {name} : {value}")
                    raise
        print(f"Добавлено растений {inserted_new}")
        print(f"Добавлено свойств: {inserted_factors}")
        print(f"Обновлено свойств: {updated_factors}")
        print()

        # Обновление родов
        cur.execute("SELECT name_ru, id FROM plants")
        plants_ids = {normalize(name): idx for name, idx in cur.fetchall()}
        cur.execute("SELECT id, genus_id FROM plants WHERE genus_id IS NOT NULL")
        plants_genera = {idx: genus_id for idx, genus_id in cur.fetchall()}
        updated_genera = 0
        for name in set(genera["Вид"]):
            if normalize(name) not in plants_ids:
                name = f"'{name}'"
                print(f"Растение {name:<40} отсутствует в базе данных, хотя указано его соовтетствие роду.")
        for _, (genus_name, plant_name) in genera[["Род", "Вид"]].iterrows():
            if (plant_name := normalize(plant_name)) in plants_ids:
                genus_name = genus_name.lower()
                if plants_genera.get(plants_ids[plant_name]) != genera_ids[genus_name]:
                    cur.execute(
                        "UPDATE plants SET genus_id = %s WHERE id = %s",
                        (genera_ids[genus_name], plants_ids[plant_name]),
                    )
                    updated_genera += 1
                    plants_genera[plants_ids[plant_name]] = genera_ids[genus_name]
        if updated_genera != 0:
            print(f"Updated {updated_genera} plants genera")

        # Вставка сочетаемостей
        inserted_straight = 0
        inserted_back = 0
        updated = 0
        for _, (genus_1, value, genus_2, comment) in cohabitation[
            ["Род", "Совместимость", "Род.1", "Краткий комментарий"]
        ].iterrows():
            genus_1, genus_2 = genus_1.lower(), genus_2.lower()
            if genus_1 in missing_genera or genus_2 in missing_genera:
                continue
            cur.execute(
                "SELECT cohabitation_type FROM cohabitation WHERE genus_id_1 = %s AND genus_id_2 = %s",
                (genera_ids[genus_1], genera_ids[genus_2]),
            )
            if (res := cur.fetchone()) is not None:
                value_now = 1 if res[0] == "positive" else 0 if res[0] == "neutral" else -1
                if value_now != value:
                    cur.execute(
                        "UPDATE cohabitation SET cohabitation_type = %s WHERE genus_id_1 = %s AND genus_id_2 = %s",
                        (
                            ("positive" if value == 1 else "neutral" if value == 0 else "negative"),
                            genera_ids[genus_1],
                            genera_ids[genus_2],
                        ),
                    )
                    updated += 1
            else:
                cur.execute(
                    "INSERT INTO cohabitation (genus_id_1, genus_id_2, cohabitation_type, comment_id) VALUES (%s, %s, %s, %s)",
                    (
                        genera_ids[genus_1],
                        genera_ids[genus_2],
                        "positive" if value == 1 else "neutral" if value == 0 else "negative",
                        comments_ids[comment] if comment in comments_ids else None,
                    ),
                )
                inserted_straight += 1
        for _, (genus_1, value, genus_2, comment) in cohabitation[
            ["Род", "Совместимость", "Род.1", "Краткий комментарий"]
        ].iterrows():
            genus_1, genus_2 = genus_1.lower(), genus_2.lower()
            if genus_1 in missing_genera or genus_2 in missing_genera:
                continue
            cur.execute(
                "SELECT cohabitation_type FROM cohabitation WHERE genus_id_1 = %s AND genus_id_2 = %s",
                (genera_ids[genus_2], genera_ids[genus_1]),
            )
            if (res := cur.fetchone()) is not None:
                value_now = 1 if res[0] == "positive" else 0 if res[0] == "neutral" else -1
                if value_now != value:
                    print(
                        f"Сочетаемость родов {genus_2:<20} и {genus_1:<20} имеет значение {value_now} напрямую и {value} в обратную сторону"
                    )
            else:
                cur.execute(
                    "INSERT INTO cohabitation (genus_id_1, genus_id_2, cohabitation_type, comment_id) VALUES (%s, %s, %s, %s)",
                    (
                        genera_ids[genus_2],
                        genera_ids[genus_1],
                        "positive" if value == 1 else "neutral" if value == 0 else "negative",
                        comments_ids[comment] if comment in comments_ids else None,
                    ),
                )
                inserted_back += 1
        print(
            f"Добавлено {inserted_straight} прямых значений совместимости + {inserted_back} обратных значений. Обновлены {updated} связей."
        )
finally:
    try:
        conn.close()
    except:
        pass
