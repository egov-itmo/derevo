"""
Main compositioning method logic is defined here.
"""
from compositioner import GlobalTerritory, Plant, Territory, get_composition, get_territory
from shapely.geometry.base import BaseGeometry
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.dto import PlantDto


async def get_global_territory(conn: AsyncConnection, geom: BaseGeometry) -> GlobalTerritory:
    """
    Collect polygons of different factors as a GlobalTerritory for the copositioner method.
    """

    # TODO: collect data from database to GeoDataFrames and pass them to GlobalTerritory()

    global_territory = GlobalTerritory()
    return global_territory


def get_territory_info(polygon: BaseGeometry, global_territory: GlobalTerritory) -> Territory:
    """
    Form a Territory object from polygon and global territory.
    """
    return get_territory(polygon, global_territory)


async def get_plants_composition(
    plants_available: list[Plant],
    territory: Territory,
    plants_present: list[Plant],
) -> list[PlantDto]:
    """
    Get plants composition that will cohabitate well with the given plants already present in the territory.
    """
    plants = get_composition(plants_available, territory, plants_present)

    # TODO: convert plants back to PlantDto
    return []
