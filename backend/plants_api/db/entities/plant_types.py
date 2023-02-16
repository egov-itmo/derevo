"""
Plants types (life forms) table is defined here.
"""
from sqlalchemy import Column, Integer, String, Table, text

from plants_api.db import metadata

plant_types = Table(
    "plant_types",
    metadata,
    Column("id", Integer, primary_key=True, server_default=text("nextval('plant_types_id_seq'::regclass)")),
    Column("name", String, nullable=False, unique=True),
)
