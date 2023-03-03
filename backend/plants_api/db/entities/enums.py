"""
Enumerations converted to database datatypes are defined here
"""

from enum import Enum


class CohabitationType(Enum):
    """
    Cohavbitation type enumeration.
    """

    negative = "negative"
    neutral = "neutral"
    positive = "positive"
