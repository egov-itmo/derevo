"""
Tables which represent part of some factor types are defined here.

Current list is: humidity_type_parts, light_type_parts, limitation_factor_type_parts
"""
from geoalchemy2.types import Geometry
from sqlalchemy import Column, ForeignKey, Integer, Sequence, Table

from plants_api.db import metadata

humidity_type_parts_id_seq = Sequence("humidity_type_parts_id_seq")

humidity_type_parts = Table(
    "humidity_type_parts",
    metadata,
    Column("id", Integer, primary_key=True, server_default=humidity_type_parts_id_seq.next_value()),
    Column("humidity_type_id", ForeignKey("humidity_types.id"), nullable=False),
    Column("geometry", Geometry("GEOMETRY", 4236, spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry")),
)
"""
Geometry parts of a different humidity options.

Columns:
- `id` - humidity_type part identifier, int serial
- `humidity_type_id` - identifier of a humidity type (humidity_types.id), int
- `geometry` - polygon, geometry
"""


light_type_parts_id_seq = Sequence("light_type_parts_id_seq")

light_type_parts = Table(
    "light_type_parts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        index=True,
        server_default=light_type_parts_id_seq.next_value(),
    ),
    Column("light_type_id", ForeignKey("light_types.id"), nullable=False),
    Column(
        "geometry",
        Geometry("GEOMETRY", 4326, from_text="ST_GeomFromEWKT", name="geometry"),
        nullable=False,
        index=True,
    ),
)
"""
Geometry parts of a different light options.

Columns:
- `id` - light_type part identifier, int serial
- `light_type_id` - identifier of a light type (light_types.id), int
- `geometry` - polygon, geometry
"""


limitation_factor_parts_id_seq = Sequence("limitation_factor_parts_id_seq")

limitation_factor_parts = Table(
    "limitation_factor_parts",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        index=True,
        server_default=limitation_factor_parts_id_seq.next_value(),
    ),
    Column("limitation_factor_id", ForeignKey("limitation_factors.id"), nullable=False),
    Column(
        "geometry", Geometry("GEOMETRY", 4326, from_text="ST_GeomFromEWKT", name="geometry"), nullable=False, index=True
    ),
)
"""
Geometry parts of a different limitation factors options.

Columns:
- `id` - limitation_factor part identifier, int serial
- `limitation_factor_id` - identifier of a limitation factor (limitation_factors.id), int
- `geometry` - polygon, geometry
"""
