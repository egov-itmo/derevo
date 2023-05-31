"""
Plant model class is defined here.
"""
from dataclasses import dataclass, field

from .enumerations import (
    AcidityType,
    AggressivenessLevel,
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
    - `name_ru` (str): russian name of the plant.
    - `name_latin` (str): latin name of the plant.
    - `genus` (str | None, *optional*): genera name of the plant, required for method but optional. Defaults to None.
    - `limitation_factors_resistances` (dict[LimitationFactor, ToleranceType], *optional*): dictionary with keys
        as limitation factors and values as a tolerance type for a plant to the given limitation factor. Defaults to {}.
    - `usda_zone_preferences` (dict[UsdaZone, ToleranceType], *optional*): dictionary with keys as USDA zones and
        values as a tolerance type for a plant to the given USDA zone. Default to {}.
    - `light_preferences` (dict[LightType, ToleranceType], *optional*): dictionary with keys as light types and
        values as a tolerance type for a plant to the given light type. Default to {}.
    - `humidity_preferences` (dict[HumidityType, ToleranceType], *optional*): dictionary with keys as humidity types
        and values as a tolerance type for a plant to the given humidity type. Default to {}.
    - `soil_acidity_preferences` (dict[AcidityType, ToleranceType], *optional*): dictionary with keys as soil acidity
        types and values as a tolerance type for a plant to the given soil acidity type. Default to {}.
    - `soil_fertility_preferences` (dict[FertilityType, ToleranceType], *optional*): dictionary with keys as soil
        fertility types and values as a tolerance type for a plant to the given soil fertility type. Default to {}.
    - `soil_type_preferences` (dict[SoilType, ToleranceType], *optional*): dictionary with keys as soil types and
        values as a tolerance type for a plant to the given soil type. Default to {}.
    """

    name_ru: str
    name_latin: str
    genus: str | None = None
    life_form: LifeForm | None = None
    limitation_factors_resistances: dict[LimitationFactor, ToleranceType] = field(default_factory=dict)
    usda_zone_preferences: dict[UsdaZone, ToleranceType] = field(default_factory=dict)
    light_preferences: dict[LightType, ToleranceType] = field(default_factory=dict)
    humidity_preferences: dict[HumidityType, ToleranceType] = field(default_factory=dict)
    soil_acidity_preferences: dict[AcidityType, ToleranceType] = field(default_factory=dict)
    soil_fertility_preferences: dict[FertilityType, ToleranceType] = field(default_factory=dict)
    soil_type_preferences: dict[SoilType, ToleranceType] = field(default_factory=dict)
    aggresiveness: AggressivenessLevel = AggressivenessLevel.NEUTRAL
    survivability: SurvivabilityLevel = SurvivabilityLevel.NORMAL
    is_invasive: bool = False

    def __str__(self) -> str:
        dict_fields = (
            ("limitation_factors_resistances: {}", self.limitation_factors_resistances),
            ("usda_zones: {}", self.usda_zone_preferences),
            ("lights: {}", self.light_preferences),
            ("humidities: {}", self.humidity_preferences),
            ("soil_acidities: {}", self.soil_acidity_preferences),
            ("soil_fertilities: {}", self.soil_fertility_preferences),
            ("soil_types: {}", self.soil_type_preferences),
        )
        dict_fields_text = ", ".join(d_f[0] for d_f in dict_fields if d_f[1])
        return (
            "Plant(name_ru='{}', name_latin='{}', genus='{}', aggressiveness={}, survivability={}"
            + (f", {dict_fields_text}" if len(dict_fields_text) != 0 else "")
            + ")"
        ).format(
            self.name_ru,
            self.name_latin,
            self.genus,
            self.aggresiveness,
            self.survivability,
            *(str(d_f[1]) for d_f in dict_fields if d_f[1]),
        )
