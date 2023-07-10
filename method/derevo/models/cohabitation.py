"""
Genus cohabitation attributes model is defined here.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Literal


class CohabitationType(Enum):
    """
    Enumeration used to two genera cohabitation.
    """

    NEGATIVE = "NEGATIVE"
    NEUTRAL = "NEUTRAL"
    POSITIVE = "POSITIVE"

    def to_value(self) -> Literal[-1, 0, 1]:
        """
        Get tolerance type as an integer value in range [-1, 1].
        """
        return -1 if self.value == CohabitationType.NEGATIVE else 0 if self.value == CohabitationType.NEUTRAL else 1

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.name


@dataclass
class GeneraCohabitation:
    """
    Contains cohabitation type of two plant genus
    """

    genus_1: str
    genus_2: str
    cohabitation: CohabitationType
