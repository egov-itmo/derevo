"""
Module to store all of the database tables.
"""

from plants_api.db.entities.climate_zones import climate_zones
from plants_api.db.entities.cohabitation import cohabitation
from plants_api.db.entities.cohabitation_comments import cohabitation_comments
from plants_api.db.entities.factor_types import (
    humidity_types,
    light_types,
    limitation_factors,
    soil_acidity_types,
    soil_fertility_types,
    soil_types,
)
from plants_api.db.entities.factor_types_parts import humidity_type_parts, light_type_parts, limitation_factor_parts
from plants_api.db.entities.features import features
from plants_api.db.entities.genera import genera
from plants_api.db.entities.plant_types import plant_types
from plants_api.db.entities.plants import plants
from plants_api.db.entities.plants_factors import (
    plants_climate_zones,
    plants_features,
    plants_humidity_types,
    plants_light_types,
    plants_limitation_factors,
    plants_soil_acidity_types,
    plants_soil_fertility_types,
    plants_soil_types,
)
from plants_api.db.entities.territories import territories

__all__ = [
    "climate_zones",
    "cohabitation",
    "cohabitation_comments",
    "humidity_types",
    "light_types",
    "limitation_factors",
    "soil_acidity_types",
    "soil_fertility_types",
    "soil_types",
    "humidity_type_parts",
    "light_type_parts",
    "limitation_factor_parts",
    "features",
    "genera",
    "plant_types",
    "plants_climate_zones",
    "plants_features",
    "plants_humidity_types",
    "plants_light_types",
    "plants_limitation_factors",
    "plants_soil_acidity_types",
    "plants_soil_fertility_types",
    "plants_soil_types",
    "plants",
    "territories",
]
