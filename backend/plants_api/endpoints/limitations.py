"""
Endpoints of user requests of limitations polygons by the given geometry.
"""
from fastapi import Depends
from pyproj import Geod
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.exceptions.logic.geometry import TooLargeGeometryError
from plants_api.logic.limitations import get_limitation_factors as get_limitation_factors_from_db
from plants_api.logic.limitations import get_light as get_light_from_db
from plants_api.schemas import GeoJSONResponse
from plants_api.schemas.geometry import GeometryPostRequest

from .routers import limitations_router

_geod = Geod(ellps="WGS84")
_AREA_MAX = 6_000_000


@limitations_router.post(
    "/limitation_factors",
    status_code=status.HTTP_200_OK,
)
async def get_limitation_factors(
    geometry: GeometryPostRequest,
    conn: AsyncConnection = Depends(get_connection),
) -> GeoJSONResponse:
    """
    Return limitation factors around the given area.
    """
    geom = geometry.as_shapely_geometry()
    if (area_given := _geod.geometry_area_perimeter(geom)[0]) > _AREA_MAX:
        raise TooLargeGeometryError(_AREA_MAX, area_given)

    return await GeoJSONResponse.from_list(await get_limitation_factors_from_db(conn, geom))


@limitations_router.post(
    "/light_factors",
    status_code=status.HTTP_200_OK,
)
async def get_light(
    geometry: GeometryPostRequest,
    conn: AsyncConnection = Depends(get_connection),
) -> GeoJSONResponse:
    """
    Return light factors around the given area.
    """
    geom = geometry.as_shapely_geometry()
    if (area_given := _geod.geometry_area_perimeter(geom)[0]) > _AREA_MAX:
        raise TooLargeGeometryError(_AREA_MAX, area_given)

    return await GeoJSONResponse.from_list(await get_light_from_db(conn, geom))
