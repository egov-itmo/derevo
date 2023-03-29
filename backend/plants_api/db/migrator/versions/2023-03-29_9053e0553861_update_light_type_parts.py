# pylint: disable=no-member,invalid-name,missing-function-docstring,too-many-statements
"""update_light_type_parts


Revision ID: 9053e0553861
Revises: 8e4f5637d763
Create Date: 2023-03-29 12:57:20.706953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9053e0553861"
down_revision = "8e4f5637d763"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_column("light_type_parts", "insolation_value")
    op.execute(sa.text("ALTER TABLE light_type_parts ALTER COLUMN geometry TYPE geometry(geometry, 4326)"))
    op.execute(sa.text("ALTER TABLE limitation_factor_parts ALTER COLUMN geometry TYPE geometry(geometry, 4326)"))


def downgrade():
    op.execute(sa.text("ALTER TABLE limitation_factor_parts ALTER COLUMN geometry TYPE geometry(polygon, 4326)"))
    op.execute(sa.text("ALTER TABLE light_type_parts ALTER COLUMN geometry TYPE geometry(multipolygon, 4326)"))
    op.add_column(
        "light_type_parts",
        sa.Column("insolation_value", sa.VARCHAR(), autoincrement=False, nullable=False, server_default=""),
    )
