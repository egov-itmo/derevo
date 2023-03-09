"""init

Revision ID: 8e4f5637d763
Revises: 
Create Date: 2023-03-02 21:40:40.241613

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = "8e4f5637d763"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    # extensions

    op.execute(sa.text("CREATE EXTENSION postgis"))

    # sequences

    op.execute(sa.schema.CreateSequence(sa.Sequence("climate_zones_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("cohabitation_comments_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("districts_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("features_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("genera_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("humidity_types_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("light_types_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("limitation_factors_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("plant_types_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("soil_acidity_types_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("soil_fertility_types_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("soil_types_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("humidity_type_parts_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("light_type_parts_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("limitation_factor_parts_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("parks_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("plants_id_seq")))
    op.execute(sa.schema.CreateSequence(sa.Sequence("territories_id_seq")))

    # tables

    op.create_table(
        "climate_zones",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('climate_zones_id_seq')"), nullable=False),
        sa.Column("usda_number", sa.Integer(), nullable=False),
        sa.Column("temperature_min", sa.Integer(), nullable=False),
        sa.Column("temperature_max", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("climate_zones_pk")),
    )
    op.create_table(
        "cohabitation_comments",
        sa.Column(
            "id", sa.Integer(), server_default=sa.text("nextval('cohabitation_comments_id_seq')"), nullable=False
        ),
        sa.Column("text", sa.String(length=250), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("cohabitation_comments_pk")),
        sa.UniqueConstraint("text", name=op.f("cohabitation_comments_text_key")),
    )
    op.create_table(
        "districts",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('districts_id_seq')"), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column("sheet_name", sa.String(length=80), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("districts_pk")),
        sa.UniqueConstraint("name", name=op.f("districts_name_key")),
        sa.UniqueConstraint("sheet_name", name=op.f("districts_sheet_name_key")),
    )
    op.create_table(
        "features",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('features_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("features_pk")),
        sa.UniqueConstraint("name", name=op.f("features_name_key")),
    )
    op.create_table(
        "genera",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('genera_id_seq')"), nullable=False),
        sa.Column("name_ru", sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("genera_pk")),
        sa.UniqueConstraint("name_ru", name=op.f("genera_name_ru_key")),
    )
    op.create_table(
        "humidity_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('humidity_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("humidity_types_pk")),
        sa.UniqueConstraint("name", name=op.f("humidity_types_name_key")),
    )
    op.create_table(
        "light_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('light_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("light_types_pk")),
        sa.UniqueConstraint("name", name=op.f("light_types_name_key")),
    )
    op.create_table(
        "limitation_factors",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('limitation_factors_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("explanation", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("limitation_factors_pk")),
        sa.UniqueConstraint("name", name=op.f("limitation_factors_name_key")),
    )
    op.create_table(
        "plant_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('plant_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("plant_types_pk")),
        sa.UniqueConstraint("name", name=op.f("plant_types_name_key")),
    )
    op.create_table(
        "soil_acidity_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('soil_acidity_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("soil_acidity_types_pk")),
        sa.UniqueConstraint("name", name=op.f("soil_acidity_types_name_key")),
    )
    op.create_table(
        "soil_fertility_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('soil_fertility_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("soil_fertility_types_pk")),
        sa.UniqueConstraint("name", name=op.f("soil_fertility_types_name_key")),
    )
    op.create_table(
        "soil_types",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('soil_types_id_seq')"), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("soil_types_pk")),
        sa.UniqueConstraint("name", name=op.f("soil_types_name_key")),
    )
    op.create_table(
        "cohabitation",
        sa.Column("genus_id_1", sa.Integer(), nullable=False),
        sa.Column("genus_id_2", sa.Integer(), nullable=False),
        sa.Column(
            "cohabitation_type", sa.Enum("negative", "neutral", "positive", name="cohabitation_type"), nullable=False
        ),
        sa.Column("comment_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["comment_id"], ["cohabitation_comments.id"], name=op.f("cohabitation_fk_comment_id__cohabitation_comments")
        ),
        sa.ForeignKeyConstraint(["genus_id_1"], ["genera.id"], name=op.f("cohabitation_fk_genus_id_1__genera")),
        sa.ForeignKeyConstraint(["genus_id_2"], ["genera.id"], name=op.f("cohabitation_fk_genus_id_2__genera")),
        sa.PrimaryKeyConstraint("genus_id_1", "genus_id_2", name=op.f("cohabitation_pk")),
    )
    op.create_table(
        "humidity_type_parts",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('humidity_type_parts_id_seq')"), nullable=False),
        sa.Column("humidity_type_id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["humidity_type_id"],
            ["humidity_types.id"],
            name=op.f("humidity_type_parts_fk_humidity_type_id__humidity_types"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("humidity_type_parts_pk")),
    )
    op.create_table(
        "light_type_parts",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('light_type_parts_id_seq')"), nullable=False),
        sa.Column("insolation_value", sa.String(), nullable=False),
        sa.Column("light_type_id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                geometry_type="MULTIPOLYGON", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["light_type_id"], ["light_types.id"], name=op.f("light_type_parts_fk_light_type_id__light_types")
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("light_type_parts_pk")),
    )
    op.create_index(op.f("ix_light_type_parts_id"), "light_type_parts", ["id"], unique=False)
    op.create_table(
        "limitation_factor_parts",
        sa.Column(
            "id", sa.Integer(), server_default=sa.text("nextval('limitation_factor_parts_id_seq')"), nullable=False
        ),
        sa.Column("limitation_factor_id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(
                geometry_type="POLYGON", srid=4326, from_text="ST_GeomFromEWKT", name="geometry"
            ),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["limitation_factor_id"],
            ["limitation_factors.id"],
            name=op.f("limitation_factor_parts_fk_limitation_factor_id__limitation_factors"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("limitation_factor_parts_pk")),
    )
    op.create_index(op.f("ix_limitation_factor_parts_id"), "limitation_factor_parts", ["id"], unique=False)
    op.create_table(
        "parks",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('parks_id_seq')"), nullable=False),
        sa.Column("district_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=80), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["district_id"], ["districts.id"], name=op.f("parks_fk_district_id__districts")),
        sa.PrimaryKeyConstraint("id", name=op.f("parks_pk")),
        sa.UniqueConstraint("district_id", "name", name=op.f("parks_district_id_name_key")),
    )
    op.create_table(
        "plants",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('plants_id_seq')"), nullable=False),
        sa.Column("name_ru", sa.String(), nullable=False),
        sa.Column("name_latin", sa.String(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=True),
        sa.Column("height_avg", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("crown_diameter", sa.Numeric(precision=3, scale=1), nullable=True),
        sa.Column("spread_aggressiveness_level", sa.Integer(), nullable=True),
        sa.Column("survivability_level", sa.Integer(), nullable=True),
        sa.Column("is_invasive", sa.Boolean(), nullable=True),
        sa.Column("genus_id", sa.Integer(), nullable=True),
        sa.Column("photo_name", sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(["genus_id"], ["genera.id"], name=op.f("plants_fk_genus_id__genera")),
        sa.ForeignKeyConstraint(["type_id"], ["plant_types.id"], name=op.f("plants_fk_type_id__plant_types")),
        sa.PrimaryKeyConstraint("id", name=op.f("plants_pk")),
        sa.UniqueConstraint("name_latin", name=op.f("plants_name_latin_key")),
        sa.UniqueConstraint("name_ru", name=op.f("plants_name_ru_key")),
    )
    op.create_table(
        "territories",
        sa.Column("id", sa.Integer(), server_default=sa.text("nextval('territories_id_seq')"), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("acidity_type_id", sa.Integer(), nullable=False),
        sa.Column("fertility_type_id", sa.Integer(), nullable=False),
        sa.Column(
            "geometry",
            geoalchemy2.types.Geometry(spatial_index=False, from_text="ST_GeomFromEWKT", name="geometry"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["acidity_type_id"],
            ["soil_acidity_types.id"],
            name=op.f("territories_fk_acidity_type_id__soil_acidity_types"),
        ),
        sa.ForeignKeyConstraint(
            ["fertility_type_id"],
            ["soil_fertility_types.id"],
            name=op.f("territories_fk_fertility_type_id__soil_fertility_types"),
        ),
        sa.ForeignKeyConstraint(["type_id"], ["soil_types.id"], name=op.f("territories_fk_type_id__soil_types")),
        sa.PrimaryKeyConstraint("id", name=op.f("territories_pk")),
    )
    op.create_table(
        "plants_climate_zones",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("climate_zone_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["climate_zone_id"],
            ["climate_zones.id"],
            name=op.f("plants_climate_zones_fk_climate_zone_id__climate_zones"),
        ),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], name=op.f("plants_climate_zones_fk_plant_id__plants")),
        sa.PrimaryKeyConstraint("plant_id", "climate_zone_id", name=op.f("plants_climate_zones_pk")),
    )
    op.create_table(
        "plants_features",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("feature_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["feature_id"], ["features.id"], name=op.f("plants_features_fk_feature_id__features")),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], name=op.f("plants_features_fk_plant_id__plants")),
        sa.PrimaryKeyConstraint("plant_id", "feature_id", name=op.f("plants_features_pk")),
    )
    op.create_table(
        "plants_humidity_types",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("humidity_type_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["humidity_type_id"],
            ["humidity_types.id"],
            name=op.f("plants_humidity_types_fk_humidity_type_id__humidity_types"),
        ),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], name=op.f("plants_humidity_types_fk_plant_id__plants")),
        sa.PrimaryKeyConstraint("plant_id", "humidity_type_id", name=op.f("plants_humidity_types_pk")),
    )
    op.create_table(
        "plants_light_types",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("light_type_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["light_type_id"], ["light_types.id"], name=op.f("plants_light_types_fk_light_type_id__light_types")
        ),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], name=op.f("plants_light_types_fk_plant_id__plants")),
        sa.PrimaryKeyConstraint("plant_id", "light_type_id", name=op.f("plants_light_types_pk")),
    )
    op.create_table(
        "plants_limitation_factors",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("limitation_factor_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["limitation_factor_id"],
            ["limitation_factors.id"],
            name=op.f("plants_limitation_factors_fk_limitation_factor_id__limitation_factors"),
        ),
        sa.ForeignKeyConstraint(
            ["plant_id"], ["plants.id"], name=op.f("plants_limitation_factors_fk_plant_id__plants")
        ),
        sa.PrimaryKeyConstraint("plant_id", "limitation_factor_id", name=op.f("plants_limitation_factors_pk")),
    )
    op.create_table(
        "plants_parks",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("park_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["park_id"], ["parks.id"], name=op.f("plants_parks_fk_park_id__parks")),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], name=op.f("plants_parks_fk_plant_id__plants")),
        sa.PrimaryKeyConstraint("plant_id", "park_id", name=op.f("plants_parks_pk")),
    )
    op.create_table(
        "plants_soil_acidity_types",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("soil_acidity_type_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["plant_id"], ["plants.id"], name=op.f("plants_soil_acidity_types_fk_plant_id__plants")
        ),
        sa.ForeignKeyConstraint(
            ["soil_acidity_type_id"],
            ["soil_acidity_types.id"],
            name=op.f("plants_soil_acidity_types_fk_soil_acidity_type_id__soil_acidity_types"),
        ),
        sa.PrimaryKeyConstraint("plant_id", "soil_acidity_type_id", name=op.f("plants_soil_acidity_types_pk")),
    )
    op.create_table(
        "plants_soil_fertility_types",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("soil_fertility_type_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["plant_id"], ["plants.id"], name=op.f("plants_soil_fertility_types_fk_plant_id__plants")
        ),
        sa.ForeignKeyConstraint(
            ["soil_fertility_type_id"],
            ["soil_fertility_types.id"],
            name=op.f("plants_soil_fertility_types_fk_soil_fertility_type_id__soil_fertility_types"),
        ),
        sa.PrimaryKeyConstraint("plant_id", "soil_fertility_type_id", name=op.f("plants_soil_fertility_types_pk")),
    )
    op.create_table(
        "plants_soil_types",
        sa.Column("plant_id", sa.Integer(), nullable=False),
        sa.Column("soil_type_id", sa.Integer(), nullable=False),
        sa.Column("is_stable", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(["plant_id"], ["plants.id"], name=op.f("plants_soil_types_fk_plant_id__plants")),
        sa.ForeignKeyConstraint(
            ["soil_type_id"], ["soil_types.id"], name=op.f("plants_soil_types_fk_soil_type_id__soil_types")
        ),
        sa.PrimaryKeyConstraint("plant_id", "soil_type_id", name=op.f("plants_soil_types_pk")),
    )

    # data

    op.execute(
        sa.text(
            "INSERT INTO climate_zones (usda_number, temperature_min, temperature_max) VALUES"
            "   (1, -90, -45),"
            "   (2, -44, -40),"
            "   (3, -39, -34),"
            "   (4, -33, -29),"
            "   (5, -28, -23),"
            "   (6, -22, -18),"
            "   (7, -17, -12),"
            "   (8, -11, -7),"
            "   (9, -6, -1),"
            "   (10, 0, 4),"
            "   (11, 5, 10),"
            "   (12, 11, 16),"
            "   (13, 17, 21)"
        )
    )

    op.execute(
        sa.text(
            "INSERT INTO soil_types (name) VALUES"
            "   ('Песчаная'),"
            "   ('Супесчаная'),"
            "   ('Суглинистая'),"
            "   ('Глинистая'),"
            "   ('Каменистые'),"
            "   ('Щебнистые'),"
            "   ('Каменистая'),"
            "   ('Тяжёлая'),"
            "   ('Хорошо дренированная')"
        )
    )

    op.execute(
        sa.text("INSERT INTO light_types (name) VALUES ('Полное освещение'), ('Полутень'), ('Тень')")
    )

    op.execute(
        sa.text(
            "INSERT INTO humidity_types (name) VALUES"
            "   ('Мало воды'),"
            "   ('Средняя'),"
            "   ('Много воды'),"
            "   ('Влажность в воздухе')"
        )
    )

    op.execute(
        sa.text(
            "INSERT INTO soil_fertility_types (name) VALUES"
            "   ('Плодородная'),"
            "   ('Средне плодородная'),"
            "   ('Бедная почва')"
        )
    )

    op.execute(
        sa.text(
            "INSERT INTO soil_acidity_types (name) VALUES"
            "   ('Сильнокислые (4)'),"
            "   ('Кислые (5)'),"
            "   ('Слабокислые (6)'),"
            "   ('Нейтральные (7)'),"
            "   ('Слабощелочные (8)'),"
            "   ('Щелочные (9)'),"
            "   ('Сильнощелочные (10)')"
        )
    )

    op.execute(
        sa.text(
            "INSERT INTO limitation_factors (name, explanation) VALUES"
            "   ('Устойчивость к переуплотнению', '...'),"
            "   ('Устойчивость к засолению', '...'),"
            "   ('Устойчивость к пересыханию', '...'),"
            "   ('Устойчивость к подтоплению', '...'),"
            "   ('Газостойкость', '...'),"
            "   ('Ветроустойчивость', '...')"
        )
    )


def downgrade():

    # tables

    op.drop_table("plants_soil_types")
    op.drop_table("plants_soil_fertility_types")
    op.drop_table("plants_soil_acidity_types")
    op.drop_table("plants_parks")
    op.drop_table("plants_limitation_factors")
    op.drop_table("plants_light_types")
    op.drop_table("plants_humidity_types")
    op.drop_table("plants_features")
    op.drop_table("plants_climate_zones")
    op.drop_table("territories")
    op.drop_table("plants")
    op.drop_table("parks")
    op.drop_index(op.f("ix_limitation_factor_parts_id"), table_name="limitation_factor_parts")
    op.drop_table("limitation_factor_parts")
    op.drop_index(op.f("ix_light_type_parts_id"), table_name="light_type_parts")
    op.drop_table("light_type_parts")
    op.drop_table("humidity_type_parts")
    op.drop_table("cohabitation")
    op.drop_table("soil_types")
    op.drop_table("soil_fertility_types")
    op.drop_table("soil_acidity_types")
    op.drop_table("plant_types")
    op.drop_table("limitation_factors")
    op.drop_table("light_types")
    op.drop_table("humidity_types")
    op.drop_table("genera")
    op.drop_table("features")
    op.drop_table("districts")
    op.drop_table("cohabitation_comments")
    op.drop_table("climate_zones")

    # sequences

    op.execute(sa.schema.DropSequence(sa.Sequence("territories_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("plants_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("parks_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("limitation_factor_parts_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("light_type_parts_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("humidity_type_parts_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("soil_types_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("soil_fertility_types_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("soil_acidity_types_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("plant_types_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("limitation_factors_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("light_types_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("humidity_types_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("genera_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("features_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("districts_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("cohabitation_comments_id_seq")))
    op.execute(sa.schema.DropSequence(sa.Sequence("climate_zones_id_seq")))

    # types

    op.execute(sa.text("DROP TYPE cohabitation_type"))

    # extensions

    op.execute(sa.text("DROP EXTENSION postgis"))
