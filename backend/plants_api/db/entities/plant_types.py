"""
Plants types (life forms) table is defined here.
"""
from sqlalchemy import Column, Integer, Sequence, String, Table

from plants_api.db import metadata

plant_types_id_seq = Sequence("plant_types_id_seq")

plant_types = Table(
    "plant_types",
    metadata,
    Column("id", Integer, primary_key=True, server_default=plant_types_id_seq.next_value()),
    Column("name", String, nullable=False, unique=True),
)
