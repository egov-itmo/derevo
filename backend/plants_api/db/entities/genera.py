"""
Plants genera (multiple form of genus) table is defined here.
"""
from sqlalchemy import Column, Integer, Sequence, String, Table

from plants_api.db import metadata

genera_id_seq = Sequence("genera_id_seq")

genera = Table(
    "genera",
    metadata,
    Column("id", Integer, primary_key=True, server_default=genera_id_seq.next_value()),
    Column("name_ru", String(100), nullable=False, unique=True),
)
