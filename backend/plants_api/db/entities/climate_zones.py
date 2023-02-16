"""
Climate zones table is defined here.
"""
from geoalchemy2.types import Geometry
from sqlalchemy import Column, Integer, Table, text

from plants_api.db import metadata

climate_zones = Table(
    "climate_zones",
    metadata,
    Column("id", Integer, primary_key=True, server_default=text("nextval('climate_zones_id_seq'::regclass)")),
    Column("usda_number", Integer, nullable=False),
    Column("temperature_min", Integer, nullable=False),
    Column("temperature_max", Integer, nullable=False),
    Column("geometry", Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry")),
)
