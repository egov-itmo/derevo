# pylint: disable=no-name-in-module, too-few-public-methods
"""
Geometry request is defined here.
"""
from loguru import logger
from pydantic import BaseModel, validator
from shapely import geometry as geom

from .geojson import Geometry


class GeometryPostRequest(BaseModel):
    """
    Geometry post request (only Polygons and MultiPolygons are accepted).
    """

    geometry: Geometry

    @validator("geometry")
    @staticmethod
    def validate_geometry(geometry: Geometry) -> None:
        """
        Validate that given geometry is Polygon or MultiPolygon (not a Point) and validity via creating Shapely object.
        """
        assert geometry.type in ("Polygon", "Multipolygon"), "Only Polygons and MultiPolygons are accepted"
        try:
            geometry.as_shapely_geometry()
        except (AttributeError, ValueError, TypeError) as exc:
            logger.debug("Exception on passing geometry: {!r}", exc)
            raise ValueError("Invalid geometry passed") from exc
        return geometry

    def as_shapely_geometry(self) -> geom.Polygon | geom.MultiPolygon:
        """
        Get requested geometry as Shapely Polygon or MultiPolygon object.
        """
        return self.geometry.as_shapely_geometry()
