"""
Plants features table is defined here.
"""
from sqlalchemy import Column, Integer, Sequence, String, Table

from plants_api.db import metadata

features_id_seq = Sequence("features_id_seq")

features = Table(
    "features",
    metadata,
    Column("id", Integer, primary_key=True, server_default=features_id_seq.next_value()),
    Column("name", String, nullable=False, unique=True),
)
"""
Plants features.

Columns:
- `id` - feature identifier, int serial
- `name` - name of the feature, varchar
"""
