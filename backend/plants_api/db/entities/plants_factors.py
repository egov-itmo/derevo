"""
Tables which represent a connection of plants and factor_types are defined here.

Current list is: plants_climate_zones, plants_features, plants_humidity_types, plants_light_types,
    plants_limitation_factors, plants_soil_acidity_types, plants_soil_fertility_types, plants_soil_types
"""
from sqlalchemy import Boolean, Column, Enum, ForeignKey, Table

from plants_api.db import metadata
from plants_api.db.entities.enums import CohabitationType


CohabitationTypeEnum = Enum(CohabitationType, name="cohabitation_type")

plants_climate_zones = Table(
    "plants_climate_zones",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column(
        "climate_zone_id",
        ForeignKey("climate_zones.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for climate zones.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `climate_zone_id` - climate zone identifier (climate_zones.id), int
- `type` - tolerance type, CohabitationType enumeration
"""


plants_features = Table(
    "plants_features",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("feature_id", ForeignKey("features.id"), primary_key=True, nullable=False),
    Column("is_stable", Boolean, nullable=False),
)
"""
Plants features.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `feature_id` - feature identifier (features.id), int
- `is_stable` - indicates whether feature is always present, boolean
"""

plants_humidity_types = Table(
    "plants_humidity_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column(
        "humidity_type_id",
        ForeignKey("humidity_types.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for humidity types.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `humidity_type_id` - humidity type identifier (humidity_types.id), int
- `type` - tolerance type, CohabitationType enumeration
"""

plants_light_types = Table(
    "plants_light_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("light_type_id", ForeignKey("light_types.id"), primary_key=True, nullable=False),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for light types.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `light_type_id` - light type identifier (light_types.id), int
- `type` - tolerance type, CohabitationType enumeration
"""

plants_limitation_factors = Table(
    "plants_limitation_factors",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column(
        "limitation_factor_id",
        ForeignKey("limitation_factors.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for limitation factors.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `limitation_factor_id` - limitation factor identifier (limitation_factors.id), int
- `type` - tolerance type, CohabitationType enumeration
"""

plants_soil_acidity_types = Table(
    "plants_soil_acidity_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column(
        "soil_acidity_type_id",
        ForeignKey("soil_acidity_types.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for soil acidity types.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `soil_acidity_type_id` - soil acidity type identifier (soil_acidity_types.id), int
- `type` - tolerance type, CohabitationType enumeration
"""

plants_soil_fertility_types = Table(
    "plants_soil_fertility_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column(
        "soil_fertility_type_id",
        ForeignKey("soil_fertility_types.id"),
        primary_key=True,
        nullable=False,
    ),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for soil acidity types.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `soil_fertility_type_id` - soil fertility type identifier (soil_fertility_types.id), int
- `type` - tolerance type, CohabitationType enumeration
"""

plants_soil_types = Table(
    "plants_soil_types",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("soil_type_id", ForeignKey("soil_types.id"), primary_key=True, nullable=False),
    Column("type", CohabitationTypeEnum, nullable=False),
)
"""
Plants suitable for soil types.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `soil_type_id` - soil type identifier (soil_types.id), int
- `type` - tolerance type, CohabitationType enumeration
"""
