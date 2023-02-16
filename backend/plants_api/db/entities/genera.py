"""
Plants genera (multiple form of genus) table is defined here.
"""
from sqlalchemy import Column, Integer, String, Table, text

from plants_api.db import metadata

genera = Table(
    "genera",
    metadata,
    Column("id", Integer, primary_key=True, server_default=text("nextval('genera_id_seq'::regclass)")),
    Column("name_ru", String(100), nullable=False, unique=True),
)
