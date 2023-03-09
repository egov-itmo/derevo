"""
Data Transfer Objects (much like entities from database) are degined in this module.
"""

from plants_api.dto.listings import ListingDto
from plants_api.dto.plants import PlantDto

__all__ = [
    "ListingDto",
    "PlantDto",
]
