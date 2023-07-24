"""
Global territory model class is defined here.
"""
from __future__ import annotations

from dataclasses import dataclass, fields
from enum import Enum
from typing import Iterable, Type

import geopandas as gpd
from loguru import logger

from derevo.models.enumerations import (
    AcidityType,
    FertilityType,
    HumidityType,
    LightType,
    LimitationFactor,
    SoilType,
    UsdaZone,
)
from derevo.models.territory import Territory


def _check_names(
    gdf: gpd.GeoDataFrame,
    concrete_enum: Type[LightType]
    | Type[LimitationFactor]
    | type[HumidityType]
    | Type[SoilType]
    | Type[AcidityType]
    | Type[FertilityType],
):
    """
    Remove rows which name cannot be cast to the given enumeration.
    """
    enums = {entry.name.lower() for entry in concrete_enum}
    if any((lf.name.lower() if isinstance(lf, Enum) else lf.lower()) not in enums for lf in gdf["name"].unique()):
        logger.warning(
            "Some {} geometries are dropped as their names are not in enum values",
            concrete_enum.__name__,
        )
        logger.debug(
            "Number of {} polygons before removal: {}",
            concrete_enum.__name__,
            gdf.shape[0],
        )
        gdf.drop(
            (
                gdf[~gdf["name"].apply(lambda lf: lf.name.lower() if isinstance(lf, Enum) else lf.lower()).isin(enums)]
            ).index,
            inplace=True,
        )
        logger.debug(
            "Number of {} polygons after removal: {}",
            concrete_enum.__name__,
            gdf.shape[0],
        )


def _names_to_enum(values: Iterable[str | Enum], concrete_enum: type[Enum]) -> list[Enum]:
    """
    Construct list of given enum types from their string names.
    """
    return [concrete_enum(v.capitalize()) if isinstance(v, str) else v for v in values]


def _names_to_unique_enum(values: Iterable[str | Enum], concrete_enum: type[Enum]) -> list[Enum]:
    """
    Construct list of given enum types from their string names.
    """
    return list({concrete_enum(v.capitalize()) if isinstance(v, str) else v for v in values})


@dataclass
class GlobalTerritory:
    """
    Global territory model (for a whole city for example) that contains all of its factors data.

    Missing or None value in init means that the parameter is unknown and will not be taken in the account.

    Fields notes:
    - `limitation_factors` GeoDataFrame must contain column 'name' with values corresponding to `LimitationFactor`
    emueration
    - `light_types` GeoDataFrame must contain column 'name' with values corresponding to `LightType` enumeration
    - `humidity_types` GeoDataFrame must contain column 'name' with values corresponding to `HumidityType` enumeration
    - `soil_types` GeoDataFrame must contain column 'name' with values corresponding to `SoilType` enumeration
    - `soil_acidity_types` GeoDataFrame must contain column 'name' with values corresponding
    to `AcidityType` enumeration
    - `soil_fertility_types` GeoDataFrame must contain column 'name' with values corresponding
    to `FertilityType` enumeration
    """

    usda_zone: UsdaZone | None = None
    limitation_factors: gpd.GeoDataFrame = ...
    light_types: gpd.GeoDataFrame = ...
    humidity_types: gpd.GeoDataFrame = ...
    soil_types: gpd.GeoDataFrame = ...
    soil_acidity_types: gpd.GeoDataFrame = ...
    soil_fertility_types: gpd.GeoDataFrame = ...

    def __post_init__(self):
        """
        Check that each of the DataFrames contains 'name' column. Throw ValueError otherwise.
        """
        for attribute in (f.name for f in fields(GlobalTerritory) if f.name != "usda_zone"):
            attr_value = getattr(self, attribute)
            if attr_value is None or attr_value is ...:
                setattr(self, attribute, gpd.GeoDataFrame(columns="name"))

        for concrete_enum, gdf in zip(
            [
                LimitationFactor,
                LightType,
                HumidityType,
                SoilType,
                AcidityType,
                FertilityType,
            ],
            [
                self.limitation_factors,
                self.light_types,
                self.humidity_types,
                self.soil_types,
                self.soil_acidity_types,
                self.soil_fertility_types,
            ],
        ):
            if "name" not in gdf.columns:
                raise ValueError(
                    f"{concrete_enum.__name__} GeoDataFrame does not contain 'name' column."
                    f" All columns provided: {', '.join(gdf.columns)}"
                )
            _check_names(gdf, concrete_enum)

    def as_territory(self) -> Territory:
        """
        Get global territory information as Territory class.
        """
        return Territory(
            self.usda_zone,
            _names_to_unique_enum(self.limitation_factors["name"], LimitationFactor),
            _names_to_unique_enum(self.light_types["name"], LightType),
            _names_to_unique_enum(self.humidity_types["name"], HumidityType),
            _names_to_unique_enum(self.soil_types["name"], SoilType),
            _names_to_unique_enum(self.soil_acidity_types["name"], AcidityType),
            _names_to_unique_enum(self.soil_fertility_types["name"], FertilityType),
        )
