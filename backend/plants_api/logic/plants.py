"""
Plants endpoints logic of getting entities from the database is defined here.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import genera, plant_types, plants
from plants_api.dto import PlantDto
from plants_api.utils import get_photo_url
from plants_api.utils.photos import get_thumbnail_url


async def get_plants_from_db(connection: AsyncConnection) -> list[PlantDto]:
    """
    Get all plants from database.
    """
    statement = (
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
        .order_by(plants.c.id)
    )
    return [
        PlantDto(
            *data,
            (get_photo_url(photo_name) if photo_name is not None else None),
            (get_thumbnail_url(photo_name) if photo_name is not None else None),
        )
        for *data, photo_name in await connection.execute(statement)
    ]
