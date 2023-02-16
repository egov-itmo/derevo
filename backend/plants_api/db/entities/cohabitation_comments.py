"""
Cohabitation comments table is defined here.
"""
from sqlalchemy import Column, Integer, String, Table, text

from plants_api.db import metadata

cohabitation_comments = Table(
    "cohabitation_comments",
    metadata,
    Column("id", Integer, primary_key=True, server_default=text("nextval('cohabitation_comments_id_seq'::regclass)")),
    Column("text", String(250), nullable=False, unique=True),
)
