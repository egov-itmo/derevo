# pylint: disable=missing-module-docstring, no-name-in-module, too-few-public-methods, duplicate-code
"""
Geojson response model and its inner parts are defined here.
"""
import json
import typing as tp
from typing import Any, Iterable

import pandas as pd
from loguru import logger
from pydantic import BaseModel
from sqlalchemy.engine.row import Row


class Crs(BaseModel):
    """
    Projection SRID / CRS representation for GeoJSON model.
    """

    type: str
    properties: dict[str, tp.Any]

    @property
    def code(self) -> int:
        """
        Return code of the projection. Would work only if CRS properties is set as name: ...<code>.
        """
        name = self.properties["name"]
        try:
            return int(name[name.rindex(":") + 1 :]) if ":" in name else int(name)
        except Exception as exc:
            logger.debug("Crs {} code is invalid? {!r}", self, exc)
            raise ValueError(f"something wrong with crs name: '{name}'") from exc


crs_4326 = Crs(type="name", properties={"name": "urn:ogc:def:crs:EPSG:4326"})
crs_3857 = Crs(type="name", properties={"name": "urn:ogc:def:crs:EPSG:3857"})


class Geometry(BaseModel):
    """
    Geometry representation for GeoJSON model.
    """

    type: tp.Literal["Point", "Polygon", "MultiPolygon", "LineString"]
    coordinates: list[tp.Any]


class Feature(BaseModel):
    """
    Feature representation for GeoJSON model.
    """

    type: tp.Literal["Feature"] = "Feature"
    geometry: Geometry
    properties: dict[str, tp.Any] = {}

    @classmethod
    def from_series(cls, series: pd.Series, geometry_column: str = "geometry", include_nulls: bool = True) -> "Feature":
        """
        Construct Feature object from series with a given geometrty column.
        """
        properties = series.to_dict()
        if not include_nulls:
            properties = {name: value for name, value in properties.items() if value is not None}
        geometry = properties[geometry_column]
        del properties[geometry_column]
        if isinstance(geometry, str):
            geometry = json.loads(geometry)
        return cls(geometry=geometry, properties=properties)

    @classmethod
    def from_dict(
        cls, feature: dict[str, Any], geometry_column: str = "geometry", include_nulls: bool = True
    ) -> "Feature":
        """
        Construct Feature object from dictionary with a given geometrty field.
        """
        properties = dict(feature)
        if not include_nulls:
            properties = {name: value for name, value in properties.items() if value is not None}
        geometry = properties[geometry_column]
        del properties[geometry_column]
        if isinstance(geometry, str):
            geometry = json.loads(geometry)
        return cls(geometry=geometry, properties=properties)

    @classmethod
    def from_row(cls, row: dict[str, Any], geometry_column: str = "geometry", include_nulls: bool = True) -> "Feature":
        """
        Construct Feature object from dictionary with a given geometrty field.
        """
        geometry = row[geometry_column]
        if isinstance(geometry, str):
            geometry = json.loads(geometry)

        if include_nulls:
            properties = {name: row[name] for name in row.keys() if name != geometry_column}
        else:
            properties = {name: row[name] for name in row.keys() if name != geometry_column and row[name] is not None}

        return cls(geometry=geometry, properties=properties)


class GeoJSONResponse(BaseModel):
    """
    GeoJSON model representation.
    """

    crs: Crs
    type: tp.Literal["FeatureCollection"] = "FeatureCollection"
    features: list[Feature]

    @classmethod
    async def from_df(
        cls, data_df: pd.DataFrame, geometry_column: str = "geometry", crs: Crs = crs_4326, include_nulls: bool = True
    ) -> "GeoJSONResponse":
        """
        Construct GeoJSON model from pandas DataFrame with one column containing GeoJSON geometries.
        """
        return cls(
            crs=crs,
            features=list(data_df.apply(lambda row: Feature.from_series(row, geometry_column, include_nulls), axis=1)),
        )

    @classmethod
    async def from_list(
        cls,
        features: Iterable[dict[str, Any]],
        geometry_field: str = "geometry",
        crs: Crs = crs_4326,
        include_nulls: bool = True,
    ) -> "GeoJSONResponse":
        """
        Construct GeoJSON model from list of dictionaries or SQLAlchemy Row classes from the database,
            with one field in each containing GeoJSON geometries.
        """

        func = Feature.from_row if isinstance(next(iter(features), None), Row) else Feature.from_dict
        features = [
            func(feature, geometry_field, include_nulls) for feature in features
        ]  # TODO: move it to another process to increase performance
        return cls(
            crs=crs,
            features=features,
        )
