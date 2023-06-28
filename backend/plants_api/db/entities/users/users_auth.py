# pylint: disable=too-many-ancestors, abstract-method
"""
Users Authentication database table is defined here.

It stores access tokens data
"""
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, Sequence, String, Table, UniqueConstraint

from plants_api.db import metadata


users_auth_id_seq = Sequence("users_auth_id_seq", schema="users")

users_auth = Table(
    "users_auth",
    metadata,
    Column("id", Integer, users_auth_id_seq, server_default=users_auth_id_seq.next_value(), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.users.id"), nullable=False),
    Column("device", String(200), nullable=False),
    Column("is_active", Boolean, nullable=False, default=True),
    Column("refresh_until", TIMESTAMP(timezone=True), nullable=False),
    Column("valid_until", TIMESTAMP(timezone=True), nullable=False),
    UniqueConstraint("user_id", "device", name="users_auth_unique_user_id_device"),
    schema="users",
)
"""
Users authentications which is used to maintain access and refresh tokens.

Columns:
- `id` - user_auth identifier, int serial
- `user_id` - identifier of the user, integer
- `device` - user device name used for refreshing token, varchar(200)
- `is_active` - indicates whether device token is deactivated even if it is still vaild by time, boolean
- `refresh_until` - datetime of a last moment by which refresh token is valid, timestamptz
- `valid_until` - datetime of a last moment by which access token is valid, timestamptz
"""
