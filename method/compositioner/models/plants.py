"""
Plant model class is defined here.
"""
from dataclasses import dataclass, field

from .enumerations import (
    AcidityType,
    AgressivenessLevel,
    FertilityType,
    HumidityType,
    LifeForm,
    LightType,
    LimitationFactor,
    SoilType,
    SurvivabilityLevel,
    ToleranceType,
    UsdaZone,
)


@dataclass
class Plant:  # pylint: disable=too-many-instance-attributes
    """
    Plant class for the compositioner methods.

    Fields:
    - `name_ru` (str): russian name of the plant
    - `name_latin` (str): latin name of the plant
    - `genus` (str): genera name of the plant
    - `limitation_factors_resistance` (dict[LimitationFactor, ToleranceType]): dictionary with keys as limitation
        factors and values as a tolerance type for a plant to the given limitation factor. Defaults to {}.
    - `usda_zone_preferences` (dict[UsdaZone, ToleranceType]): dictionary with keys as USDA zones and values as a
        tolerance type for a plant to the given USDA zone. Default to {}.
    - `light_preferences` (dict[LightType, ToleranceType]): dictionary with keys as light types and values as a
        tolerance type for a plant to the given light type. Default to {}.
    - `humidity_preferences` (dict[HumidityType, ToleranceType]): dictionary with keys as humidity types and values
        as a tolerance type for a plant to the given humidity type. Default to {}.
    - `soil_acidity_preferences` (dict[AcidityType, ToleranceType]): dictionary with keys as soil acidity types and
        values as a tolerance type for a plant to the given soil acidity type. Default to {}.
    - `soil_fertility_preferences` (dict[FertilityType, ToleranceType]): dictionary with keys as soil fertility
        types and values as a tolerance type for a plant to the given soil fertility type. Default to {}.
    - `soil_type_preferences` (dict[SoilType, ToleranceType]): dictionary with keys as soil types and
        values as a tolerance type for a plant to the given soil type. Default to {}.
    """

    name_ru: str
    name_latin: str
    genus: str
    life_form: LifeForm | None = None
    limitation_factors_resistances: dict[LimitationFactor, ToleranceType] = field(default_factory=dict)
    usda_zone_preferences: dict[UsdaZone, ToleranceType] = field(default_factory=dict)
    light_preferences: dict[LightType, ToleranceType] = field(default_factory=dict)
    humidity_preferences: dict[HumidityType, ToleranceType] = field(default_factory=dict)
    soil_acidity_preferences: dict[AcidityType, ToleranceType] = field(default_factory=dict)
    soil_fertility_preferences: dict[FertilityType, ToleranceType] = field(default_factory=dict)
    soil_type_preferences: dict[SoilType, ToleranceType] = field(default_factory=dict)
    aggresiveness: AgressivenessLevel = AgressivenessLevel.NEUTRAL
    survivability: SurvivabilityLevel = SurvivabilityLevel.NORMAL
    is_invasive: bool = False
