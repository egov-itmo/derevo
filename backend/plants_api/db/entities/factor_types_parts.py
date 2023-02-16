"""
Tables which represent part of some factor types are defined here.

Current list is: humidity_type_parts, light_type_parts, limitation_factor_type_parts
"""
from geoalchemy2.types import Geometry
from sqlalchemy import Column, ForeignKey, Integer, String, Table, text

from plants_api.db import metadata

humidity_type_parts = Table(
    "humidity_type_parts",
    metadata,
    Column("id", Integer, primary_key=True, server_default=text("nextval('humidity_type_parts_id_seq'::regclass)")),
    Column("humidity_type_id", ForeignKey("humidity_types.id"), nullable=False),
    Column("geometry", Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry")),
)

light_type_parts = Table(
    "light_type_parts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        index=True,
        server_default=text("nextval('light_type_parts_id_seq'::regclass)"),
    ),
    Column("insolation_value", String, nullable=False),
    Column("light_type_id", ForeignKey("light_types.id"), nullable=False),
    Column(
        "geometry",
        Geometry("MULTIPOLYGON", 4326, from_text="ST_GeomFromEWKT", name="geometry"),
        nullable=False,
        index=True,
    ),
)

limitation_factor_parts = Table(
    "limitation_factor_parts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        index=True,
        server_default=text("nextval('limitation_factor_parts_id_seq'::regclass)"),
    ),
    Column("limitation_factor_id", ForeignKey("limitation_factors.id"), nullable=False),
    Column(
        "geometry", Geometry("POLYGON", 4326, from_text="ST_GeomFromEWKT", name="geometry"), nullable=False, index=True
    ),
)
