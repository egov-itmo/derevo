"""
Main compositioning method logic is defined here.
"""
import geopandas as gpd
from derevo import GeneraCohabitation, GlobalTerritory, Plant, Territory
from derevo import enumerations as c_enum
from derevo import get_compositions
from derevo import get_territory as cm_get_territory
from loguru import logger
from shapely.geometry.base import BaseGeometry
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.util import greenlet_spawn

from plants_api.db.entities import (
    humidity_type_parts,
    humidity_types,
    light_type_parts,
    light_types,
    limitation_factor_parts,
    limitation_factors,
    soil_acidity_types,
    soil_fertility_types,
    soil_types,
    territories,
)
from plants_api.dto import PlantDto
from plants_api.logic.plants import get_plants_by_name_ru
from plants_api.utils.adapters.derevo_enums import EnumAdapters

_cached_global_territory: GlobalTerritory | None = None


async def get_global_territory(conn: AsyncConnection, use_cached: bool = True) -> GlobalTerritory:
    """
    Collect polygons of different factors as a GlobalTerritory for the copositioner method.

    Collects once and uses cached version unless `use_cache` is not set to False.
    """
    global _cached_global_territory  # pylint: disable=invalid-name,global-statement
    if use_cached and _cached_global_territory is not None:
        logger.debug(
            "Using cached global territory with the next number of polygons: {} limitation factor,"
            " {} light type, {} humidity type,"
            " and {} territory (soil + acidity + fertility)",
            _cached_global_territory.limitation_factors.shape[0],
            _cached_global_territory.light_types.shape[0],
            _cached_global_territory.humidity_types.shape[0],
            _cached_global_territory.soil_types.shape[0],
        )
        return _cached_global_territory

    logger.debug("Getting global territory")
    usda_zone = c_enum.UsdaZone.USDA5  # hard-coded for now

    lf_gdf = await greenlet_spawn(
        lambda: gpd.read_postgis(
            select(limitation_factors.c.name, limitation_factor_parts.c.geometry)
            .select_from(limitation_factors)
            .join(
                limitation_factor_parts,
                limitation_factors.c.id == limitation_factor_parts.c.limitation_factor_id,
            ),
            conn.sync_engine,
            geom_col="geometry",
        )
    )
    lf_gdf["name"] = lf_gdf["name"].apply(EnumAdapters.limitation_factors.get)
    lf_gdf = lf_gdf.dropna(subset="name")

    lt_gdf = await greenlet_spawn(
        lambda: gpd.read_postgis(
            select(light_types.c.name, light_type_parts.c.geometry)
            .select_from(light_types)
            .join(light_type_parts, light_types.c.id == light_type_parts.c.light_type_id),
            conn.sync_engine,
            geom_col="geometry",
        )
    )
    lt_gdf["name"] = lt_gdf["name"].apply(EnumAdapters.light.get)
    lt_gdf = lt_gdf.dropna(subset="name")

    ht_gdf = await greenlet_spawn(
        lambda: gpd.read_postgis(
            select(humidity_types.c.name, humidity_type_parts.c.geometry)
            .select_from(humidity_types)
            .join(
                humidity_type_parts,
                humidity_types.c.id == humidity_type_parts.c.humidity_type_id,
            ),
            conn.sync_engine,
            geom_col="geometry",
        )
    )
    ht_gdf["name"] = ht_gdf["name"].apply(EnumAdapters.humidity.get)
    ht_gdf = ht_gdf.dropna(subset="name")

    terr_gdf = await greenlet_spawn(
        lambda: gpd.read_postgis(
            select(
                soil_types.c.name.label("soil_type"),
                soil_acidity_types.c.name.label("acidity_type"),
                soil_fertility_types.c.name.label("fertility_type"),
                territories.c.geometry,
            )
            .select_from(territories)
            .join(soil_types, soil_types.c.id == territories.c.type_id)
            .join(
                soil_acidity_types,
                soil_acidity_types.c.id == territories.c.acidity_type_id,
            )
            .join(
                soil_fertility_types,
                soil_fertility_types.c.id == territories.c.fertility_type_id,
            ),
            conn.sync_engine,
            geom_col="geometry",
        )
    )
    terr_gdf["soil_type"] = terr_gdf["soil_type"].apply(EnumAdapters.soil.get)
    terr_gdf["acidity_type"] = terr_gdf["acidity_type"].apply(EnumAdapters.acidity.get)
    terr_gdf["fertility_type"] = terr_gdf["fertility_type"].apply(EnumAdapters.fertility.get)

    global_territory = GlobalTerritory(
        usda_zone,
        lf_gdf,
        lt_gdf,
        ht_gdf,
        terr_gdf[["soil_type", "geometry"]].rename({"soil_type": "name"}, axis=1).dropna(subset="name"),
        terr_gdf[["acidity_type", "geometry"]].rename({"acidity_type": "name"}, axis=1).dropna(subset="name"),
        terr_gdf[["fertility_type", "geometry"]].rename({"fertility_type": "name"}, axis=1).dropna(subset="name"),
    )
    _cached_global_territory = global_territory
    logger.debug(
        "Global territory has next number of polygons: {} limitation factor, {} light type, {} humidity type,"
        " and {} territory (soil + acidity + fertility)",
        lf_gdf.shape[0],
        lt_gdf.shape[0],
        ht_gdf.shape[0],
        terr_gdf.shape[0],
    )
    return global_territory


def get_territory(polygon: BaseGeometry, global_territory: GlobalTerritory) -> Territory:
    """
    Form a Territory object from polygon and global territory.
    """
    return cm_get_territory(polygon, global_territory)


async def get_plants_compositions(
    conn: AsyncConnection,
    plants_available: list[Plant],
    territory: Territory,
    cohabitation_attributes: list[GeneraCohabitation],
    plants_present: list[Plant],
) -> list[list[PlantDto]]:
    """
    Get plants composition that will cohabitate well with the given plants already present in the territory.
    """
    compositions = get_compositions(plants_available, territory, cohabitation_attributes, plants_present)

    return [await get_plants_by_name_ru(conn, [p.name_ru for p in composition]) for composition in compositions]
