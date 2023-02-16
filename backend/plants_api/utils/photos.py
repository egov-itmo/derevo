"""
get_photo_url function is defined here.
"""

from plants_api.config.app_settings_global import app_settings


def get_photo_url(photo_name: str) -> str:
    return f"{app_settings.photos_prefix}{photo_name}"
