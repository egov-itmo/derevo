"""
Enumerations converted to database datatypes are defined here
"""

from enum import Enum


class CohabitationType(Enum):
    """
    Cohavbitation type enumeration.
    """

    negative = "negative"  # pylint: disable=invalid-name
    neutral = "neutral"  # pylint: disable=invalid-name
    positive = "positive"  # pylint: disable=invalid-name
