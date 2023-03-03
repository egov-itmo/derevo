"""
Territories table is defined here.

Territory is a piece of land with a known soil_type, soil_acididy_type and soil_fertility_type
"""
from geoalchemy2.types import Geometry
from sqlalchemy import Column, ForeignKey, Integer, Table, Sequence

from plants_api.db import metadata

territories_id_seq = Sequence("territories_id_seq")

territories = Table(
    "territories",
    metadata,
    Column("id", Integer, primary_key=True, server_default=territories_id_seq.next_value()),
    Column("type_id", ForeignKey("soil_types.id"), nullable=False),
    Column("acidity_type_id", ForeignKey("soil_acidity_types.id"), nullable=False),
    Column("fertility_type_id", ForeignKey("soil_fertility_types.id"), nullable=False),
    Column("geometry", Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry")),
)
