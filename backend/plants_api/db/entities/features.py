"""
Plants features table is defined here.
"""
from sqlalchemy import Column, Integer, String, Table, text

from plants_api.db import metadata

features = Table(
    "features",
    metadata,
    Column("id", Integer, primary_key=True, server_default=text("nextval('features_id_seq'::regclass)")),
    Column("name", String, nullable=False, unique=True),
)
