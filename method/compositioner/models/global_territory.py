"""
Global territory model class is defined here.
"""
from dataclasses import dataclass

import geopandas as gpd

from compositioner.models.enumerations import UsdaZone


@dataclass
class GlobalTerritory:
    """
    Global territory model (for a whole city for example) that contains all of its factors data.

    None value means that the parameter is unknown and will not be taken in the account.

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
    limitation_factors: gpd.GeoDataFrame | None = None
    light_types: gpd.GeoDataFrame | None = None
    humidity_types: gpd.GeoDataFrame | None = None
    soil_types: gpd.GeoDataFrame | None = None
    soil_acidity_types: gpd.GeoDataFrame | None = None
    soil_fertility_types: gpd.GeoDataFrame | None = None
