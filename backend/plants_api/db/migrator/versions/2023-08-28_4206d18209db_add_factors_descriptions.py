# pylint: disable=no-member,invalid-name,missing-function-docstring,too-many-statements
"""Add outer factors description column, rename explanation of limitation_factors

Revision ID: 4206d18209db
Revises: 82cb5d6e072b
Create Date: 2023-08-28 16:05:34.417381

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = "4206d18209db"
down_revision = "82cb5d6e072b"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("limitation_factors", "explanation", new_column_name="description")
    op.add_column("humidity_types", sa.Column("description", sa.String(), nullable=True))
    op.add_column("light_types", sa.Column("description", sa.String(), nullable=True))
    op.add_column("soil_acidity_types", sa.Column("description", sa.String(), nullable=True))
    op.add_column("soil_fertility_types", sa.Column("description", sa.String(), nullable=True))
    op.add_column("soil_types", sa.Column("description", sa.String(), nullable=True))

    op.execute(sa.text("UPDATE humidity_types SET description = ''"))
    op.execute(sa.text("UPDATE light_types SET description = ''"))
    op.execute(sa.text("UPDATE soil_acidity_types SET description = ''"))
    op.execute(sa.text("UPDATE soil_fertility_types SET description = ''"))
    op.execute(sa.text("UPDATE soil_types SET description = ''"))

    op.execute(
        sa.text(
            "UPDATE soil_acidity_types SET description = 'ph=4', name = 'Сильнокислые' WHERE name = 'Сильнокислые (4)'"
        )
    )
    op.execute(sa.text("UPDATE soil_acidity_types SET description = 'ph=5', name = 'Кислые' WHERE name = 'Кислые (5)'"))
    op.execute(
        sa.text(
            "UPDATE soil_acidity_types SET description = 'ph=6', name = 'Слабокислые' WHERE name = 'Слабокислые (6)'"
        )
    )
    op.execute(
        sa.text(
            "UPDATE soil_acidity_types SET description = 'ph=7', name = 'Нейтральные' WHERE name = 'Нейтральные (7)'"
        )
    )
    op.execute(
        sa.text(
            "UPDATE soil_acidity_types SET description = 'ph=8', name = 'Слабощелочные'"
            " WHERE name = 'Слабощелочные (8)'"
        )
    )
    op.execute(
        sa.text("UPDATE soil_acidity_types SET description = 'ph=9', name = 'Щелочные' WHERE name = 'Щелочные (9)'")
    )
    op.execute(
        sa.text(
            "UPDATE soil_acidity_types SET description = 'ph=10', name = 'Сильнощелочные'"
            " WHERE name = 'Сильнощелочные (10)'"
        )
    )

    op.execute(sa.text("UPDATE humidity_types SET name = 'Пересыхающая земля' WHERE name = 'Мало воды'"))
    op.execute(sa.text("UPDATE humidity_types SET name = 'Нормальная влажность' WHERE name = 'Средняя'"))
    op.execute(sa.text("UPDATE humidity_types SET name = 'Влажная земля' WHERE name = 'Много воды'"))

    op.alter_column("humidity_types", "description", nullable=False)
    op.alter_column("light_types", "description", nullable=False)
    op.alter_column("soil_acidity_types", "description", nullable=False)
    op.alter_column("soil_fertility_types", "description", nullable=False)
    op.alter_column("soil_types", "description", nullable=False)


def downgrade():
    op.execute(sa.text("UPDATE humidity_types SET name = 'Мало воды' WHERE name = 'Пересыхающая земля'"))
    op.execute(sa.text("UPDATE humidity_types SET name = 'Средняя' WHERE name = 'Нормальная влажность'"))
    op.execute(sa.text("UPDATE humidity_types SET name = 'Много воды' WHERE name = 'Влажная земля'"))

    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Сильнокислые (4)' WHERE name = 'Сильнокислые'"))
    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Кислые (5)' WHERE name = 'Кислые'"))
    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Слабокислые (6)' WHERE name = 'Слабокислые'"))
    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Нейтральные (7)' WHERE name = 'Нейтральные'"))
    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Слабощелочные (8)' WHERE name = 'Слабощелочные'"))
    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Щелочные (9)' WHERE name = 'Щелочные'"))
    op.execute(sa.text("UPDATE soil_acidity_types SET name = 'Сильнощелочные (10)' WHERE name = 'Сильнощелочные'"))

    op.drop_column("soil_types", "description")
    op.drop_column("soil_fertility_types", "description")
    op.drop_column("soil_acidity_types", "description")
    op.drop_column("light_types", "description")
    op.drop_column("humidity_types", "description")
    op.alter_column("limitation_factors", "description", new_column_name="explanation")
