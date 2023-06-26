# pylint: disable=too-few-public-methods,no-name-in-module
"""
Limitation factors insertion request is defined here.
"""
from pydantic import BaseModel

from plants_api.dto.update.limitation_factors import LimitationFactorGeometryDto
from plants_api.schemas.geojson import Geometry


class LimitationFactorGeometry(BaseModel):
    """
    Limitation factor geometry to be inserted in the database.
    """

    geometry: Geometry
    limitation_factor_id: int

    def to_dto(self) -> LimitationFactorGeometryDto:
        """
        Construct DTO from entity leaving id=None (which is incorrect type for int).
        """
        return LimitationFactorGeometryDto(
            id=None, limitation_factor_id=self.limitation_factor_id, geometry=self.geometry.as_shapely_geometry()
        )


class LimitationFactorsGeometryInsertionRequest(BaseModel):
    """
    Limitation factors geometry insertion request.
    """

    limitation_factors: list[LimitationFactorGeometry]

    def to_dto(self) -> list[LimitationFactorGeometryDto]:
        """
        Construct DTOs list from entity.
        """
        return [lf.to_dto() for lf in self.limitation_factors]
