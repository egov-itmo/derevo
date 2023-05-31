"""
Territory-related methods are defined here.
"""
from shapely.geometry.base import BaseGeometry

from compositioner.models import GlobalTerritory, Territory


def get_territory(
    greenery_polygon: BaseGeometry,
    global_territory: GlobalTerritory,
    territory_data: Territory | None = None,
) -> Territory:
    """
    !!! THIS IS A MOCK METHOD !!! TODO: add logic

    Get territory information based on its geometry, used-defined known data and other factors polygons.
    """
    if territory_data is None:
        territory_data = Territory()

    ...

    return territory_data
