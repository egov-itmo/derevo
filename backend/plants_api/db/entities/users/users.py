# pylint: disable=too-many-ancestors, abstract-method
"""
Users database table is defined here.
"""
from sqlalchemy import CHAR, TIMESTAMP, Boolean, Column, Integer, Sequence, String, Table, UniqueConstraint, func, text

from plants_api.db import metadata

users_id_seq = Sequence("users_id_seq", schema="users")

users = Table(
    "users",
    metadata,
    Column("id", Integer, users_id_seq, server_default=users_id_seq.next_value(), primary_key=True),
    Column("email", String(64), nullable=False),
    Column("is_approved", Boolean, server_default=text("false"), nullable=False),
    Column("password_hash", CHAR(64), nullable=False),
    Column(
        "registered_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),  # pylint: disable=not-callable
    ),
    UniqueConstraint("email", name="users_unique_email"),
    schema="users",
)
"""
plants defect types.

Columns:
- `id` - user identifier, int serial
- `email` - user email address, varchar(64)
- `is_approved` - indicates whether user status is approved to update data, boolean
- `password_hash` - user password hashed with salt, varchar(128)
- `registrated_at` - user registration datetime, timestamptz
"""
