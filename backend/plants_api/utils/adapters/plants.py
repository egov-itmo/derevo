"""
PlantDTO to derevo.Plant adapter is defined here.
"""

from derevo import Plant
from derevo import enumerations as c_enum
from loguru import logger
from sqlalchemy import bindparam, select
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import (
    climate_zones,
    humidity_types,
    light_types,
    limitation_factors,
    plants_climate_zones,
    plants_humidity_types,
    plants_light_types,
    plants_limitation_factors,
    plants_soil_acidity_types,
    plants_soil_fertility_types,
    plants_soil_types,
    soil_acidity_types,
    soil_fertility_types,
    soil_types,
)
from plants_api.db.entities.enums import CohabitationType
from plants_api.dto.plants import PlantDto

from .derevo_enums import EnumAdapters

_cohabitation_type_to_tolerance_types = {
    CohabitationType.negative: c_enum.ToleranceType.NEGATIVE,
    CohabitationType.neutral: c_enum.ToleranceType.NEUTRAL,
    CohabitationType.positive: c_enum.ToleranceType.POSITIVE,
    None: None,
}


async def plant_dto_to_derevo_plant(  # pylint: disable=too-many-locals,too-many-statements
    conn: AsyncConnection, plants: list[PlantDto]
) -> list[Plant]:
    """
    Transform plant DTOs list to list of derevo Plant types.
    """
    if len(plants) == 0:
        return []

    limitation_factors_statement = select(
        select(limitation_factors.c.name)
        .where(limitation_factors.c.id == plants_limitation_factors.c.limitation_factor_id)
        .scalar_subquery(),
        plants_limitation_factors.c.type,
    ).where(plants_limitation_factors.c.plant_id == bindparam("plant_id"))
    humidity_statement = select(
        select(humidity_types.c.name)
        .where(humidity_types.c.id == plants_humidity_types.c.humidity_type_id)
        .scalar_subquery(),
        plants_humidity_types.c.type,
    ).where(plants_humidity_types.c.plant_id == bindparam("plant_id"))
    light_statement = select(
        select(light_types.c.name).where(light_types.c.id == plants_light_types.c.light_type_id).scalar_subquery(),
        plants_light_types.c.type,
    ).where(plants_light_types.c.plant_id == bindparam("plant_id"))
    soil_acidity_statement = select(
        select(soil_acidity_types.c.name)
        .where(soil_acidity_types.c.id == plants_soil_acidity_types.c.soil_acidity_type_id)
        .scalar_subquery(),
        plants_soil_acidity_types.c.type,
    ).where(plants_soil_acidity_types.c.plant_id == bindparam("plant_id"))
    soil_fertility_statement = select(
        select(soil_fertility_types.c.name)
        .where(soil_fertility_types.c.id == plants_soil_fertility_types.c.soil_fertility_type_id)
        .scalar_subquery(),
        plants_soil_fertility_types.c.type,
    ).where(plants_soil_fertility_types.c.plant_id == bindparam("plant_id"))
    soil_type_statement = select(
        select(soil_types.c.name).where(soil_types.c.id == plants_soil_types.c.soil_type_id).scalar_subquery(),
        plants_soil_types.c.type,
    ).where(plants_soil_types.c.plant_id == bindparam("plant_id"))
    usda_zone_statement = select(
        select(climate_zones.c.usda_number)
        .where(climate_zones.c.id == plants_climate_zones.c.climate_zone_id)
        .scalar_subquery(),
        plants_climate_zones.c.type,
    ).where(plants_climate_zones.c.plant_id == bindparam("plant_id"))

    plants_out: list[Plant] = []

    for plant in plants:
        if plant.genus is None:
            continue
        payload = {"plant_id": plant.id}
        try:
            life_form = EnumAdapters.life_forms.get(plant.type)

            res = list(await conn.execute(limitation_factors_statement, payload))
            limitation_factors_resistances = {
                EnumAdapters.limitation_factors.get(lf): _cohabitation_type_to_tolerance_types[value]
                for lf, value in res
            }
            if None in limitation_factors_resistances:
                logger.warning(
                    "Some of the limitation factors was not found in mapping for plant with id={}",
                    plant.id,
                )
                del limitation_factors_resistances[None]

            res = list(await conn.execute(humidity_statement, payload))
            humidity_preferences = {
                EnumAdapters.humidity.get(ht): _cohabitation_type_to_tolerance_types[value] for ht, value in res
            }
            if None in humidity_preferences:
                logger.warning(
                    "Some of the humidity types was not found in mapping for plant with id={}",
                    plant.id,
                )
                del humidity_preferences[None]

            res = list(await conn.execute(light_statement, payload))
            light_preferences = {
                EnumAdapters.light.get(lt): _cohabitation_type_to_tolerance_types[value] for lt, value in res
            }
            if None in light_preferences:
                logger.warning(
                    "Some of the light types was not found in mapping for plant with id={}",
                    plant.id,
                )
                del light_preferences[None]

            res = list(await conn.execute(soil_acidity_statement, payload))
            soil_acidity_preferences = {
                EnumAdapters.acidity.get(lt): _cohabitation_type_to_tolerance_types[value] for lt, value in res
            }
            if None in soil_acidity_preferences:
                logger.warning(
                    "Some of the soil acidity types was not found in mapping for plant with id={}",
                    plant.id,
                )
                del soil_acidity_preferences[None]

            res = list(await conn.execute(soil_fertility_statement, payload))
            soil_fertility_preferences = {
                EnumAdapters.fertility.get(lt): _cohabitation_type_to_tolerance_types[value] for lt, value in res
            }
            if None in soil_fertility_preferences:
                logger.warning(
                    "Some of the soil fertility types was not found in mapping for plant with id={}",
                    plant.id,
                )
                del soil_fertility_preferences[None]

            res = list(await conn.execute(soil_type_statement, payload))
            soil_type_preferences = {
                EnumAdapters.soil.get(lt): _cohabitation_type_to_tolerance_types[value] for lt, value in res
            }
            if None in soil_type_preferences:
                logger.warning(
                    "Some of the soil  types was not found in mapping for plant with id={}",
                    plant.id,
                )
                del soil_type_preferences[None]

            res = list(await conn.execute(usda_zone_statement, payload))
            usda_zone_preferences = {
                c_enum.UsdaZone.from_value(uz): _cohabitation_type_to_tolerance_types[value] for uz, value in res
            }
            if None in usda_zone_preferences:
                logger.warning(
                    "Some of the usda zones was not found in mapping for plant with id={}",
                    plant.id,
                )
                del usda_zone_preferences[None]

            plants_out.append(
                Plant(
                    plant.name_ru,
                    plant.name_latin,
                    plant.genus,
                    life_form,
                    limitation_factors_resistances,
                    usda_zone_preferences,
                    light_preferences,
                    humidity_preferences,
                    soil_acidity_preferences,
                    soil_fertility_preferences,
                    soil_type_preferences,
                    (
                        c_enum.AggressivenessLevel.from_value(plant.spread_aggressiveness_level)
                        if plant.spread_aggressiveness_level is not None
                        else None
                    ),
                    (
                        c_enum.SurvivabilityLevel.from_value(plant.survivability_level)
                        if plant.survivability_level is not None
                        else None
                    ),
                    plant.is_invasive,
                )
            )
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(
                "Could not transform PlantDTO with id={} to derevo.Plant: {!r}",
                plant.id,
                exc,
            )
            logger.debug("PlantDto data: {}", plant)

    return plants_out
