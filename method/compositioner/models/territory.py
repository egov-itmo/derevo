"""
Territory model class is defined here.
"""
from dataclasses import dataclass

from compositioner.models.enumerations import (
    AcidityType,
    FertilityType,
    HumidityType,
    LightType,
    LimitationFactor,
    SoilType,
    UsdaZone,
)


@dataclass
class Territory:
    """
    Description of the territory for composition creation.

    None value means that the parameter is unknown and will not be taken in the account.
    """

    usda_zone: UsdaZone | None = None
    limitation_factors: list[LimitationFactor] | None = None
    light_types: list[LightType] | None = None
    humidity_types: list[HumidityType] | None = None
    soil_types: list[SoilType] | None = None
    soil_acidity_types: list[AcidityType] | None = None
    soil_fertility_types: list[FertilityType] | None = None
