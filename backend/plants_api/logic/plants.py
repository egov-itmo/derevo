"""
Plants endpoints logic of getting entities from the database is defined here.
"""

from derevo import CohabitationType as CmCohabitationType, Plant
from derevo import GeneraCohabitation
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import cohabitation, genera, plant_types, plants
from plants_api.db.entities.enums import CohabitationType
from plants_api.dto import PlantDto
from plants_api.utils import get_photo_url
from plants_api.utils.adapters.plants import plant_dto_to_derevo_plant
from plants_api.utils.photos import get_thumbnail_url

_select_plants = (
    select(
        plants.c.id,
        plants.c.name_ru,
        plants.c.name_latin,
        plant_types.c.name.label("type"),
        plants.c.height_avg,
        plants.c.crown_diameter,
        plants.c.spread_aggressiveness_level,
        plants.c.survivability_level,
        plants.c.is_invasive,
        genera.c.name_ru.label("genus"),
        plants.c.photo_name,
    )
    .select_from(plants)
    .join(plant_types, plants.c.type_id == plant_types.c.id)
    .join(genera, plants.c.genus_id == genera.c.id)
)


async def get_plants_by_ids(conn: AsyncConnection, ids: list[int]) -> list[PlantDto]:
    """
    Get plants with given list of identifier values.
    """
    statement = _select_plants.where(plants.c.id.in_(ids)).order_by(plants.c.id)
    return [
        PlantDto(
            *data,
            (get_photo_url(photo_name) if photo_name is not None else None),
            (get_thumbnail_url(photo_name) if photo_name is not None else None),
        )
        for *data, photo_name in await conn.execute(statement)
    ]


async def get_plants_by_name_ru(conn: AsyncConnection, names_ru: list[str]) -> list[PlantDto]:
    """
    Get plants with given list of name_ru values.
    """
    statement = _select_plants.where(plants.c.name_ru.in_(names_ru))
    return [
        PlantDto(
            *data,
            (get_photo_url(photo_name) if photo_name is not None else None),
            (get_thumbnail_url(photo_name) if photo_name is not None else None),
        )
        for *data, photo_name in await conn.execute(statement)
    ]


_cached_plants_derevo: list[Plant] | None = None


async def get_plants_derevo(conn: AsyncConnection, use_cached: bool = True) -> list[Plant]:
    """
    Return all database plants as a list of `derevo.Plant` classes.
    """
    global _cached_plants_derevo  # pylint: disable=invalid-name,global-statement
    if use_cached and _cached_plants_derevo is not None:
        logger.debug("Using cached derevo plants list")
        return _cached_plants_derevo
    logger.debug("Getting plants list")
    _cached_plants_derevo = await plant_dto_to_derevo_plant(conn, await get_plants_from_db(conn))
    return _cached_plants_derevo


async def get_plants_from_db(conn: AsyncConnection) -> list[PlantDto]:
    """
    Get all plants from database.
    """
    statement = _select_plants.order_by(plants.c.id)
    return [
        PlantDto(
            *data,
            (get_photo_url(photo_name) if photo_name is not None else None),
            (get_thumbnail_url(photo_name) if photo_name is not None else None),
        )
        for *data, photo_name in await conn.execute(statement)
    ]


_cached_genera_cohabitation: list[GeneraCohabitation] | None = None


async def get_genera_cohabitation(conn: AsyncConnection, use_cached: bool = True) -> list[GeneraCohabitation]:
    """
    Get all genus cohabitations from database.
    """
    global _cached_genera_cohabitation  # pylint: disable=invalid-name,global-statement
    if use_cached and _cached_genera_cohabitation is not None:
        logger.debug("Using cached genera cohabitation data")
        return _cached_genera_cohabitation

    logger.debug("Getting genera cohabitation data from database")
    genera_1 = genera.alias("genera_1")
    genera_2 = genera.alias("genera_2")
    statement = (
        select(genera_1.c.name_ru, genera_2.c.name_ru, cohabitation.c.cohabitation_type)
        .select_from(cohabitation)
        .join(genera_1, cohabitation.c.genus_id_1 == genera_1.c.id)
        .join(genera_2, cohabitation.c.genus_id_1 == genera_2.c.id)
        .order_by(genera_1.c.name_ru, genera_2.c.name_ru)
    )
    enum_adapter = {
        CohabitationType.negative: CmCohabitationType.NEGATIVE,
        CohabitationType.neutral: CmCohabitationType.NEUTRAL,
        CohabitationType.positive: CmCohabitationType.POSITIVE,
    }
    _cached_genera_cohabitation = [
        GeneraCohabitation(genus_1, genus_2, enum_adapter[cohabitation_type])
        for genus_1, genus_2, cohabitation_type in await conn.execute(statement)
    ]
    return _cached_genera_cohabitation
