"""
Cohabitation comments table is defined here.
"""
from sqlalchemy import Column, Integer, Sequence, String, Table

from plants_api.db import metadata

cohabitation_comments_id_seq = Sequence("cohabitation_comments_id_seq")

cohabitation_comments = Table(
    "cohabitation_comments",
    metadata,
    Column("id", Integer, primary_key=True, server_default=cohabitation_comments_id_seq.next_value()),
    Column("text", String(250), nullable=False, unique=True),
)
