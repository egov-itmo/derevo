"""
Cohabitation table is defined here.
"""
from sqlalchemy import Column, Enum, ForeignKey, Table

from plants_api.db import metadata

cohabitation = Table(
    "cohabitation",
    metadata,
    Column("genus_id_1", ForeignKey("genera.id"), primary_key=True, nullable=False),
    Column("genus_id_2", ForeignKey("genera.id"), primary_key=True, nullable=False),
    Column("cohabitation_type", Enum("negative", "neutral", "positive", name="cohabitation_type"), nullable=False),
    Column("comment_id", ForeignKey("cohabitation_comments.id")),
)
