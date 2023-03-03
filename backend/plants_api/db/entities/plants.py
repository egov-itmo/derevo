"""
Plants table is defined here.
"""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, Sequence, String, Table

from plants_api.db import metadata

plants_id_seq = Sequence("plants_id_seq")

plants = Table(
    "plants",
    metadata,
    Column("id", Integer, primary_key=True, server_default=plants_id_seq.next_value()),
    Column("name_ru", String, nullable=False, unique=True),
    Column("name_latin", String, nullable=False, unique=True),
    Column("type_id", ForeignKey("plant_types.id")),
    Column("height_avg", Numeric(3, 1)),
    Column("crown_diameter", Numeric(3, 1)),
    Column("spread_aggressiveness_level", Integer),
    Column("survivability_level", Integer),
    Column("is_invasive", Boolean),
    Column("genus_id", ForeignKey("genera.id")),
    Column("photo_name", String(256)),
)
