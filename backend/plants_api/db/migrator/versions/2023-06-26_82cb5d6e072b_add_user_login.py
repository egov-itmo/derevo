# pylint: disable=no-member,invalid-name,missing-function-docstring,too-many-statements
"""add user login

Revision ID: 82cb5d6e072b
Revises: c6406a0db588
Create Date: 2023-06-26 17:35:25.559146

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "82cb5d6e072b"
down_revision = "c6406a0db588"
branch_labels = None
depends_on = None


def upgrade():
    op.execute(sa.schema.CreateSchema("users"))
    op.execute(sa.schema.CreateSequence(sa.Sequence("users_id_seq", schema="users")))
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('users.users_id_seq')"), nullable=False),
        sa.Column("email", sa.String(length=64), nullable=False),
        sa.Column("is_approved", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("password_hash", sa.CHAR(length=64), nullable=False),
        sa.Column("registered_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pk")),
        sa.UniqueConstraint("email", name="users_unique_email"),
        schema="users",
    )

    op.execute(sa.schema.CreateSequence(sa.Sequence("users_auth_id_seq", schema="users")))
    op.create_table(
        "users_auth",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('users.users_auth_id_seq')"), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("device", sa.String(length=200), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("refresh_until", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("valid_until", sa.TIMESTAMP(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.users.id"], name=op.f("users_auth_fk_user_id__users")),
        sa.PrimaryKeyConstraint("id", name=op.f("users_auth_pk")),
        sa.UniqueConstraint("user_id", "device", name="users_auth_unique_user_id_device"),
        schema="users",
    )


def downgrade():
    op.drop_table("users_auth", schema="users")
    op.execute(sa.schema.DropSequence(sa.Sequence("users_auth_id_seq", schema="users")))
    op.drop_table("users", schema="users")
    op.execute(sa.schema.DropSequence(sa.Sequence("users_id_seq", schema="users")))
    op.execute(sa.schema.DropSchema("users"))
