"""
Enumeration models are defined here.
"""
from enum import Enum
from typing import Literal


class ToleranceType(Enum):
    """
    Enumeration used to describe plant resistance to some factor.
    """

    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"

    @classmethod
    def from_value(cls, value: Literal[-1, 0, 1]) -> "ToleranceType":
        """
        Construct ToleranceType from integer value.
        """
        if value == -1:
            return ToleranceType.NEGATIVE
        if value == 0:
            return ToleranceType.NEUTRAL
        if value == 1:
            return ToleranceType.POSITIVE
        raise ValueError(f"'{value}' is not a valid ToleranceType integer value (-1, 0, 1)")


class LightType(Enum):
    """
    Enumeration used to describe possible light types.
    """

    DARK = "DARK"
    DARKENED = "DARKENED"
    LIGHT = "LIGHT"


class AcidityType(Enum):
    """
    Enumeration used to describe soil acidity types.
    """

    STRONGLY_ACIDIC = 3
    ACIDIC = 5
    SLIGHTLY_ACIDIC = 6
    NEUTRAL = 7
    SLIGHTLY_ALCALINE = 8
    ALCALINE = 9
    STRONGLY_ALCALINE = 11

    @classmethod
    def from_value(cls, value: int) -> "AcidityType":  # pylint: disable=too-many-return-statements
        """
        Construct AcidityType from pH value.

        Values:
        - <=3 - `STRONGLY_ACIDIC`
        - 4..5 - `ACIDIC`
        - 6 - `SLIGHTLY_ACIDIC`
        - 7 - `NEUTRAl`
        - 8 - `SLIGHTLY_ALCALINE`
        - 9..10 - `ALCALINE`
        - >=11 - `STRONGLY_ALCALINE`
        """
        if value <= 3:
            return AcidityType.STRONGLY_ACIDIC
        if value < 5:
            return AcidityType.ACIDIC
        if value == 6:
            return AcidityType.SLIGHTLY_ACIDIC
        if value == 7:
            return AcidityType.NEUTRAL
        if value == 8:
            return AcidityType.SLIGHTLY_ALCALINE
        if value in (9, 10):
            return AcidityType.ALCALINE
        return AcidityType.STRONGLY_ALCALINE


class FertilityType(Enum):
    """
    Enumeration used to describe soil fertility types.
    """

    BARREN = "BARREN"
    SLIGHTLY_FERTIL = "SLIGHTLY_FERTIL"
    FERTIL = "FERTIL"


class SoilType(Enum):
    """
    Enumeration used to describe soil types.
    """

    SANDY = "SANDY"
    SUBSANDY = "SUBSANDY"
    LOAMY = "LOAMY"
    CLAYEY = "CLAYEY"
    ROCKY = "ROCKY"
    GRAVELLY = "GRAVELLY"
    HEAVY = "HEAVY"
    DRAINED = "DRAINED"


class HumidityType(Enum):
    """
    Enumeration used to describe humidity types.
    """

    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class LimitationFactor(Enum):
    """
    Enumeration used to describe limitation factor.
    """

    OVERCONSOLIDATION = "OVERCONSOLIDATION"
    SALINIZATION = "SALINIZATION"
    DROUGHT = "DROUGHT"
    FLOODING = "FLOODING"
    GAS_POLLUTION = "GAS_POLLUTION"
    WINDINESS = "WINDINESS"


class UsdaZone(Enum):
    """
    Enueration used to describe USDA zones.
    """

    USDA1 = "USDA1"
    USDA2 = "USDA2"
    USDA3 = "USDA3"
    USDA4 = "USDA4"
    USDA5 = "USDA5"
    USDA6 = "USDA6"
    USDA7 = "USDA7"
    USDA8 = "USDA8"
    USDA9 = "USDA9"
    USDA10 = "USDA10"
    USDA11 = "USDA11"

    @classmethod
    def from_value(cls, value: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]) -> "UsdaZone":
        """
        Construct UsdaZone from integer value. Valid values are integers in range [1, 11].
        """
        if not isinstance(value, int) or not 1 <= value <= 11:
            raise ValueError(f"'{value}' is not a valid UsdaZone integer value intrange[1, 11]")
        return cls(f"USDA{value}")


class AgressivenessLevel(Enum):
    """
    Enumeration used to describe plant spread agressiveness.
    """

    AGGRESSIVE = "AGGRESSIVE"
    NEUTRAL = "NEUTRAL"
    SUPPRESSED = "SUPPRESSED"

    @classmethod
    def from_value(cls, value: Literal[-1, 0, 1]) -> "AgressivenessLevel":
        """
        Construct AgressivenessLevel from integer value.

        Values:
        - -1 - `SUPPRESSED`
        - 0 - `NEUTRAL`
        - 1 - `AGGRESSIVE`
        """
        if value == -1:
            return AgressivenessLevel.SUPPRESSED
        if value == 0:
            return AgressivenessLevel.NEUTRAL
        if value == 1:
            return AgressivenessLevel.AGGRESSIVE
        raise ValueError(f"'{value}' is not a valid AgressivenessLevel integer value (-1, 0, 1)")


class SurvivabilityLevel(Enum):
    """
    Enumeration used to describe plant spread agressiveness.
    """

    STRONG = "STRONG"
    NORMAL = "NORMAL"
    WEAK = "WEAK"

    @classmethod
    def from_value(cls, value: Literal[-1, 0, 1]) -> "SurvivabilityLevel":
        """
        Construct SurvivabilityLevel from integer value.

        Values:
        - -1 - `WEAK`
        - 0 - `NORMAL`
        - 1 - `STRONG`
        """
        if value == -1:
            return SurvivabilityLevel.WEAK
        if value == 0:
            return SurvivabilityLevel.NORMAL
        if value == 1:
            return SurvivabilityLevel.WEAK
        raise ValueError(f"'{value}' is not a valid SurvivabilityLevel integer value (-1, 0, 1)")


class LifeForm(Enum):
    """
    Enumeration used to describe plant life form.
    """

    TREE = "TREE"
    BUSH = "BUSH"
    GROUND_COVER = "GROUND_COVER"
    LIANA = "LIANA"
    PERENNIAL = "PERENNIAL"
    BULBOUS = "BULBOUS"
    ANNUAL = "ANNUAL"
    SWAMP_PLANT = "SWAMP_PLANT"
