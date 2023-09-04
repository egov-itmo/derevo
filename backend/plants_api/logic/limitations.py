"""
Logic of user requests of limitations polygons by the given geometry is defined here.
"""

import json
from typing import Any

from geoalchemy2 import Geography, Geometry
from geoalchemy2.functions import ST_AsGeoJSON
from shapely import geometry as geom
from sqlalchemy import cast, func, select, text
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import light_type_parts, light_types, limitation_factor_parts, limitation_factors


async def get_limitation_factors(conn: AsyncConnection, geometry: geom.Polygon | geom.MultiPolygon) -> dict[str, Any]:
    """
    Select limitation factors polygons with names.
    """
    buffered_geom = select(
        cast(
            func.ST_Buffer(
                cast(
                    func.ST_SetSRID(func.ST_GeometryFromText(geometry.wkt), text("4326")), Geography("GEOMETRY", 4326)
                ),
                text("200"),
            ),
            Geometry("GEOMETRY", "4326"),
        ).label("geometry")
    ).cte("buffered_geom")
    statement = (
        select(
            limitation_factor_parts.c.id,
            limitation_factors.c.name,
            ST_AsGeoJSON(
                func.ST_Intersection(
                    limitation_factor_parts.c.geometry, select(buffered_geom.c.geometry).scalar_subquery()
                )
            ),
        )
        .select_from(limitation_factors)
        .join(limitation_factor_parts, limitation_factor_parts.c.limitation_factor_id == limitation_factors.c.id)
        .where(func.ST_Intersects(limitation_factor_parts.c.geometry, select(buffered_geom.c.geometry).as_scalar()))
    )
    return [{"id": idx, "name": name, "geometry": geom} for idx, name, geom in await conn.execute(statement)]


async def get_all_limitation_factors(conn: AsyncConnection, limitation_factor_type_id: int) -> list[dict[str, Any]]:
    """
    Get all limitation factor polygons of a given type.
    """
    statement = select(limitation_factor_parts.c.id, ST_AsGeoJSON(limitation_factor_parts.c.geometry)).where(
        limitation_factor_parts.c.limitation_factor_id == limitation_factor_type_id
    )
    return [{"id": idx, "geometry": json.loads(geom)} for idx, geom in await conn.execute(statement)]


async def get_light(conn: AsyncConnection, geometry: geom.Polygon | geom.MultiPolygon) -> dict[str, Any]:
    """
    Select light polygons with names.
    """
    buffered_geom = select(
        cast(
            func.ST_Buffer(
                cast(
                    func.ST_SetSRID(func.ST_GeometryFromText(geometry.wkt), text("4326")), Geography("GEOMETRY", "4326")
                ),
                text("200"),
            ),
            Geometry("GEOMETRY", "4326"),
        ).label("geometry")
    ).cte("buffered_geom")
    statement = (
        select(
            light_types.c.id,
            light_types.c.name,
            ST_AsGeoJSON(
                func.ST_Intersection(light_type_parts.c.geometry, select(buffered_geom.c.geometry).scalar_subquery())
            ),
        )
        .select_from(light_types)
        .join(light_type_parts, light_type_parts.c.light_type_id == light_types.c.id)
        .where(func.ST_Intersects(light_type_parts.c.geometry, select(buffered_geom.c.geometry).scalar_subquery()))
    )
    return [{"id": idx, "name": name, "geometry": geom} for idx, name, geom in await conn.execute(statement)]
