"""
Tables referenced to parks and their plants are defined here
"""
from geoalchemy2.types import Geometry
from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table, UniqueConstraint

from plants_api.db import metadata

districts_id_seq = Sequence("districts_id_seq")

districts = Table(
    "districts",
    metadata,
    Column("id", Integer, primary_key=True, server_default=districts_id_seq.next_value()),
    Column("name", String(80), nullable=False, unique=True),
    Column("sheet_name", String(80), nullable=False, unique=True),
    Column("geometry", Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry")),
)
"""
Districts of the city to group parks.

Columns:
- `id` - district identifier, int serial
- `name` - name of the district, varchar
- `sheet_name` - name of the excel sheet to pull district parks data from, varchar
- `geometry` - district geometry if available, geometry
"""


parks_id_seq = Sequence("parks_id_seq")

parks = Table(
    "parks",
    metadata,
    Column("id", Integer, primary_key=True, server_default=parks_id_seq.next_value()),
    Column("district_id", ForeignKey("districts.id"), nullable=False),
    Column("name", String(80), nullable=False),
    Column("geometry", Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry")),
    UniqueConstraint("district_id", "name"),
)
"""
Parks of the city.

Columns:
- `id` - park identifier, int serial
- `district_id` - district identifier (districts.id), int serial
- `name` - name of the park, varchar
- `geometry` - park geometry if available, geometry
"""


plants_parks = Table(
    "plants_parks",
    metadata,
    Column("plant_id", ForeignKey("plants.id"), primary_key=True, nullable=False),
    Column("park_id", ForeignKey("parks.id"), primary_key=True, nullable=False),
)
"""
Plants inside parks.

Columns:
- `plant_id` - plant identifier (plants.id), int
- `park_id` - park identifier (parks.id)
"""
