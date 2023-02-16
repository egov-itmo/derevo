"""
Plant DTO is defined here.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class PlantDto:
    """
    Plants Dto used to transfer Plant data
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
