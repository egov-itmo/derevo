# pylint: disable=no-name-in-module, too-few-public-methods
"""
Plants responses are defined here.
"""
from typing import Optional

from pydantic import BaseModel

from plants_api.dto import PlantDto


class Plant(BaseModel):
    """
    Plant with all its attributes.
    """

    id: int
    name_ru: str
    name_latin: str
    type: Optional[str]
    height_avg: Optional[float]
    crown_diameter: Optional[float]
    spread_aggressiveness_level: Optional[int]
    survivability_level: Optional[int]
    is_invasive: Optional[bool]
    genus: Optional[str]
    photo_url: Optional[str]
    thumbnail_url: Optional[str]

    @classmethod
    def from_dto(cls, dto: PlantDto) -> "Plant":
        """
        Construct from DTO.
        """
        return cls(
            id=dto.id,
            name_ru=dto.name_ru,
            name_latin=dto.name_latin,
            type=dto.type,
            height_avg=dto.height_avg,
            crown_diameter=dto.crown_diameter,
            spread_aggressiveness_level=dto.spread_aggressiveness_level,
            survivability_level=dto.survivability_level,
            is_invasive=dto.is_invasive,
            genus=dto.genus,
            photo_url=dto.photo_url,
            thumbnail_url=dto.thumbnail_url,
        )


class PlantsResponse(BaseModel):
    """
    List of plants.
    """

    plants: list[Plant]

    @classmethod
    def from_dtos(cls, dtos: list[PlantDto]) -> "PlantsResponse":
        """
        Construct from DTOs list.
        """
        return cls(plants=[Plant.from_dto(dto) for dto in dtos])
