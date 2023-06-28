"""
Limitation factors geometry insertion logic is defined here.
"""
from sqlalchemy import bindparam, delete, exists, func, insert, select, text
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import limitation_factor_parts, limitation_factors
from plants_api.dto.update.limitation_factors import LimitationFactorGeometryDto
from plants_api.exceptions.logic.db import UnsatisfiedIdDependencyError


async def insert_limitation_factors(
    conn: AsyncConnection, limitation_factors_list: list[LimitationFactorGeometryDto]
) -> list[int]:
    """
    Insert given limitation factors list to the database.

    Returns list of inserted identitfiers.
    """
    limitation_factors_used = set(lf.limitation_factor_id for lf in limitation_factors_list)
    statement = select(
        *(
            exists().where(limitation_factors.c.id == chapter_id).label(str(chapter_id))
            for chapter_id in limitation_factors_used
        )
    )
    missing = [name for name, value in (await conn.execute(statement)).mappings().one().items() if not value]
    if len(missing) != 0:
        raise UnsatisfiedIdDependencyError(
            missing[0] if len(missing) == 1 else f"[{', '.join(missing)}]", "limitation_factors"
        )

    statement = (
        insert(limitation_factor_parts)
        .values(
            geometry=func.ST_SetSRID(func.ST_GeomFromText(bindparam("geometry_wkt")), text("4326")),
        )
        .returning(limitation_factor_parts.c.id)
    )
    ids = list(
        (
            await conn.execute(
                statement,
                [
                    {"limitation_factor_id": lf.limitation_factor_id, "geometry_wkt": lf.geometry.wkt}
                    for lf in limitation_factors_list
                ],
            )
        ).scalars()
    )

    await conn.commit()

    return ids


async def delete_limitation_factors(conn: AsyncConnection, limitation_factors_ids: list[int]) -> None:
    """
    Delete limitation factors with given ids from the database.
    """
    statement = delete(limitation_factor_parts).where(limitation_factor_parts.c.id.in_(limitation_factors_ids))
    await conn.execute(statement)

    await conn.commit()
