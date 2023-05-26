"""
get_photo_url function is defined here.
"""

from PIL import Image

from plants_api.config.app_settings_global import app_settings


def get_photo_url(photo_name: str) -> str:
    """
    Get photo url with prefix from settings.
    """
    return f"{app_settings.photos_prefix}{photo_name}"


def get_thumbnail_url(photo_name: str) -> str:
    """
    Get photo thumbnail url with prefix from settings.
    """
    return f"{app_settings.photos_prefix}thumbnails/{photo_name}"


def get_thumbnail(photo: Image.Image) -> Image.Image:
    """
    Get a photo thumbnail of a size no more than 200x200.
    """
    thumbnail = photo.copy()
    thumbnail.thumbnail((200, 200))
    return thumbnail
