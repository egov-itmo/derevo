"""
Limitation factor geometry DTO is defined here.
"""
from dataclasses import dataclass

import shapely.geometry as geom


@dataclass(frozen=True)
class LimitationFactorGeometryDto:
    """
    This DTO is used by listing endpoints logic.
    """

    id: int  # pylint: disable=invalid-name
    limitation_factor_id: int
    geometry: geom.Polygon | geom.MultiPolygon
