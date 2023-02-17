"""
Tables referenced to parks and their plants are defined here
"""
from geoalchemy2.types import Geometry
from sqlalchemy import Column, ForeignKey, Integer, String, Table, text

from plants_api.db import metadata

districts = Table(
    "districts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        index=True,
        server_default=text("nextval('districts_id_seq'::regclass)"),
    ),
    Column("name", String, nullable=False),
    Column("sheet_name", String, nullable=False),
    Column(
        "geometry",
        Geometry(srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
        nullable=False,
        index=True,
    ),
)

parks = Table(
    "parks",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        index=True,
        server_default=text("nextval('districts_id_seq'::regclass)"),
    ),
    Column("name", String, nullable=False),
    Column("district_id", Integer, ForeignKey("districts.id"), nullable=False),
    Column(
        "geometry",
        Geometry(srid=4326, from_text="ST_GeomFromEWKT", name="geometry"),
        nullable=False,
        index=True,
    ),
)

plants_parks = Table(
    "plants_parks",
    metadata,
    Column("plant_id", Integer, ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("parks_id", Integer, ForeignKey("parks.id"), primary_key=True, nullable=False),
)