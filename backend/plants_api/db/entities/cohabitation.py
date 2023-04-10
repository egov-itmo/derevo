"""
Cohabitation table is defined here.
"""
from sqlalchemy import Column, Enum, ForeignKey, Table

from plants_api.db import metadata

from .enums import CohabitationType

cohabitation = Table(
    "cohabitation",
    metadata,
    Column("genus_id_1", ForeignKey("genera.id"), primary_key=True, nullable=False),
    Column("genus_id_2", ForeignKey("genera.id"), primary_key=True, nullable=False),
    Column("cohabitation_type", Enum(CohabitationType, name="cohabitation_type"), nullable=False),
    Column("comment_id", ForeignKey("cohabitation_comments.id")),
)
"""
Plants genera cohabitations.

Columns:
- `genus_id_1` - identifier of one genus, int
- `genus_id_2` - identifier of another genus, int
- `cohabitation_type` - type of the cohabitation, CohabitationType enumeration
- `comment_id` - identifier of the cohabitation comment (cohabitation_comments.id), int
"""
