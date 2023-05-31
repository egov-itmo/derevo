# pylint: disable=wrong-import-position
"""
Compositioner module helps to create optimal plants compositions taking into an account their
cohabitations and possible limitation factors
"""

__all__ = [
    "get_composition",
    "GlobalTerritory",
    "Plant",
    "Territory",
    "enumerations",
    "get_territory",
]

import os

if "USE_PYGEOS" not in os.environ:
    os.environ["USE_PYGEOS"] = "0"  # remove this if some Shapely 2.0 incompatibility is found

from compositioner.composition import get_composition
from compositioner.models import GlobalTerritory, Plant, Territory, enumerations
from compositioner.territories import get_territory
