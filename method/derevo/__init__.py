# pylint: disable=wrong-import-position
"""
Derevo module helps to create optimal plants compositions taking into an account their
cohabitations and possible limitation factors
"""

__all__ = [
    "get_compositions",
    "Compatability",
    "GeneraCohabitation",
    "GlobalTerritory",
    "Plant",
    "Territory",
    "enumerations",
    "CohabitationType",
    "get_territory",
]

import os

os.environ["USE_PYGEOS"] = os.environ.get("USE_PYGEOS", "0")  # remove this if some Shapely 2.0 incompatibility is found

from derevo.composition import get_compositions
from derevo.models import Compatability, GeneraCohabitation, GlobalTerritory, Plant, Territory, enumerations
from derevo.models.cohabitation import CohabitationType
from derevo.territories import get_territory
