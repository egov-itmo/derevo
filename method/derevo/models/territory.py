"""
Territory model class is defined here.
"""
from __future__ import annotations

from dataclasses import dataclass, fields

from derevo.models.enumerations import (
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

    def update(self, other: "Territory", replace: bool = False) -> None:
        """
        Add `other` territory attributes to the currently set attributes. If `replace` is set to True, then
        replace current territory values whre `other` attributes are not None.
        """
        self.usda_zone = other.usda_zone
        for attribute in (f.name for f in fields(Territory) if f.name != "usda_zone"):
            update: list | None = getattr(other, attribute)
            if update is None:
                continue
            if replace:
                setattr(self, attribute, update)
            else:
                current: list | None = getattr(self, attribute)
                if current is None:
                    setattr(self, attribute, update)
                current.extend((value for value in update if value not in current))
                setattr(self, attribute, current)
