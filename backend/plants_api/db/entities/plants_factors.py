"""
Tables which represent a connection of plants and factor_types are defined here.

Current list is: plants_climate_zones, plants_features, plants_humidity_types, plants_light_types,
    plants_limitation_factors, plants_soil_acidity_types, plants_soil_fertility_types, plants_soil_types
"""
from sqlalchemy import Boolean, Column, ForeignKey, Table

from plants_api.db import metadata

plants_climate_zones = Table(
    "plants_climate_zones",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("climate_zone_id", ForeignKey("climate_zones.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_features = Table(
    "plants_features",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("feature_id", ForeignKey("features.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_humidity_types = Table(
    "plants_humidity_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("humidity_type_id", ForeignKey("humidity_types.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_light_types = Table(
    "plants_light_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("light_type_id", ForeignKey("light_types.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_limitation_factors = Table(
    "plants_limitation_factors",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("limitation_factor_id", ForeignKey("limitation_factors.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_soil_acidity_types = Table(
    "plants_soil_acidity_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("soil_acidity_type_id", ForeignKey("soil_acidity_types.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_soil_fertility_types = Table(
    "plants_soil_fertility_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("soil_fertility_type_id", ForeignKey("soil_fertility_types.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)

plants_soil_types = Table(
    "plants_soil_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("soil_type_id", ForeignKey("soil_types.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)
