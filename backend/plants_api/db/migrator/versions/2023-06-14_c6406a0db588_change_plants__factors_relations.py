# pylint: disable=no-member,invalid-name,missing-function-docstring,too-many-statements
"""change plants_<factors> relations

Revision ID: c6406a0db588
Revises: 9053e0553861
Create Date: 2023-06-14 12:56:18.026547

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "c6406a0db588"
down_revision = "9053e0553861"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "plants_climate_zones",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_climate_zones"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_climate_zones", "type", nullable=False)

    op.drop_column("plants_climate_zones", "is_stable")
    op.add_column(
        "plants_humidity_types",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_humidity_types"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_humidity_types", "type", nullable=False)
    op.drop_column("plants_humidity_types", "is_stable")

    op.add_column(
        "plants_light_types",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_light_types"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_light_types", "type", nullable=False)
    op.drop_column("plants_light_types", "is_stable")

    op.add_column(
        "plants_limitation_factors",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_limitation_factors"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_limitation_factors", "type", nullable=False)
    op.drop_column("plants_limitation_factors", "is_stable")

    op.add_column(
        "plants_soil_acidity_types",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_soil_acidity_types"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_soil_acidity_types", "type", nullable=False)
    op.drop_column("plants_soil_acidity_types", "is_stable")

    op.add_column(
        "plants_soil_fertility_types",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_soil_fertility_types"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_soil_fertility_types", "type", nullable=False)
    op.drop_column("plants_soil_fertility_types", "is_stable")

    op.add_column(
        "plants_soil_types",
        sa.Column(
            "type",
            sa.Enum("negative", "neutral", "positive", name="cohabitation_type"),
            nullable=True,
        ),
    )
    op.execute(
        sa.text(
            "UPDATE plants_soil_types"
            "   SET type = CASE"
            "       WHEN is_stable = True THEN 'positive'::cohabitation_type"
            "       ELSE 'neutral'::cohabitation_type"
            "   END"
        )
    )
    op.alter_column("plants_soil_types", "type", nullable=False)
    op.drop_column("plants_soil_types", "is_stable")
    # ### end Alembic commands ###


def downgrade():
    op.execute(sa.text("DELETE FROM plants_soil_types WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_soil_types",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_soil_types SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_soil_types", "is_stable", nullable=False)
    op.drop_column("plants_soil_types", "type")

    op.execute(sa.text("DELETE FROM plants_soil_fertility_types WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_soil_fertility_types",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_soil_fertility_types SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_soil_fertility_types", "is_stable", nullable=False)
    op.drop_column("plants_soil_fertility_types", "type")

    op.execute(sa.text("DELETE FROM plants_soil_acidity_types WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_soil_acidity_types",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_soil_acidity_types SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_soil_acidity_types", "is_stable", nullable=False)
    op.drop_column("plants_soil_acidity_types", "type")

    op.execute(sa.text("DELETE FROM plants_limitation_factors WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_limitation_factors",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_limitation_factors SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_limitation_factors", "is_stable", nullable=False)
    op.drop_column("plants_limitation_factors", "type")

    op.execute(sa.text("DELETE FROM plants_light_types WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_light_types",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_light_types SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_light_types", "is_stable", nullable=False)
    op.drop_column("plants_light_types", "type")

    op.execute(sa.text("DELETE FROM plants_humidity_types WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_humidity_types",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_humidity_types SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_humidity_types", "is_stable", nullable=False)
    op.drop_column("plants_humidity_types", "type")

    op.execute(sa.text("DELETE FROM plants_climate_zones WHERE type = 'negative'::cohabitation_type"))
    op.add_column(
        "plants_climate_zones",
        sa.Column("is_stable", sa.BOOLEAN(), autoincrement=False, nullable=True),
    )
    op.execute(sa.text("UPDATE plants_climate_zones SET is_stable = (type = 'positive'::cohabitation_type)"))
    op.alter_column("plants_climate_zones", "is_stable", nullable=False)
    op.drop_column("plants_climate_zones", "type")
    # ### end Alembic commands ###
