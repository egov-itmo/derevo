"""
Plants responses are defined here.
"""

from pydantic import BaseModel

from plants_api.dto import PlantDto
from plants_api.schemas.plants import PlantsResponse


class CompositionsResponse(BaseModel):
    """
    Compositions model containing multiple compositions each of which contains multiple plants.
    """

    compositions: list[PlantsResponse]

    @classmethod
    def from_dtos(cls, dtos: list[list[PlantDto]]) -> "PlantsResponse":
        """
        Construct from list of Plant DTOs list.
        """
        return cls(compositions=[PlantsResponse.from_dtos(plants_dtos) for plants_dtos in dtos])
