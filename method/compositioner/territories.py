"""
Territory-related methods are defined here.
"""
from shapely.geometry.base import BaseGeometry
import geopandas as gpd

from compositioner.models import GlobalTerritory, Territory


def _geom_func(gdf: gpd.GeoDataFrame, geom: BaseGeometry) -> gpd.GeoDataFrame:
    """
    Return rows of GeoDataFrame which geometry is covered by, covers or intersect the given geometry.
    """
    return gdf[gdf.covered_by(geom) | gdf.covers(geom) | gdf.intersects(geom)]


def get_territory(
    greenery_polygon: BaseGeometry,
    global_territory: GlobalTerritory,
    territory_data: Territory | None = None,
) -> Territory:
    """
    Get territory information based on its geometry, used-defined known data and other factors polygons.
    """
    if territory_data is None:
        territory_data = Territory()

    local_territory = GlobalTerritory(
        global_territory.usda_zone,
        _geom_func(global_territory.limitation_factors, greenery_polygon),
        _geom_func(global_territory.light_types, greenery_polygon),
        _geom_func(global_territory.humidity_types, greenery_polygon),
        _geom_func(global_territory.soil_types, greenery_polygon),
        _geom_func(global_territory.soil_acidity_types, greenery_polygon),
        _geom_func(global_territory.soil_fertility_types, greenery_polygon),
    )

    territory = local_territory.as_territory()
    territory.update(territory_data)

    return territory
