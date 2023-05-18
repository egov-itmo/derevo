"""
Plants photos update logic is defined here
"""

from pathlib import Path

from PIL import Image
from loguru import logger
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities import plants
from plants_api.config.app_settings_global import app_settings
from plants_api.logic.exceptions.common import DependencyNotFoundById
from plants_api.utils.photos import get_thumbnail


async def set_photo_to_plant(conn: AsyncConnection, plant_id: int, photo: Image.Image) -> None:
    """
    Update plant photo name in the database and add photo with its thumbnail to photos directory.
    """
    statement = select(plants.c.photo_name).where(plants.c.id == plant_id)
    old_photo_name = (await conn.execute(statement)).first()
    if old_photo_name is None:
        raise DependencyNotFoundById(plant_id, "plant")
    old_photo_name: str = old_photo_name[0]
    new_photo_name = f"{plant_id}.jpg"
    statement = update(plants).values(photo_name=new_photo_name).where(plants.c.id == plant_id)
    await conn.execute(statement)
    photo.save(Path(app_settings.photos_dir) / new_photo_name, quality=95)
    get_thumbnail(photo).save(Path(app_settings.photos_dir) / "thumbnails" / new_photo_name, quality=95)
    if old_photo_name is not None and old_photo_name != new_photo_name:
        logger.info("Removing old photo for the plant with id={} - {}", plant_id, old_photo_name)
        (Path(app_settings.photos_dir) / old_photo_name).unlink(missing_ok=True)
        (Path(app_settings.photos_dir) / "thumbnails" / old_photo_name).unlink(missing_ok=True)
    await conn.commit()
