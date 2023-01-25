create extension postgis;

-- basics

CREATE TABLE plant_types (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
);

-- CREATE TABLE height_categories (
--     id Serial PRIMARY KEY NOT NULL,
--     name varchar UNIQUE NOT NULL,
--     explanation varchar,      -- ?
--     height_min numeric(4, 2), -- not int
--     height_max numeric(4, 2),
--     height_avg numeric(4, 2)
-- );

-- CREATE TABLE decoratives (
--     id Serial PRIMARY KEY NOT NULL,
--     level integer NOT NULL,
--     season varchar NOT NULL
-- );

CREATE TABLE bloss_periods (
    id Serial PRIMARY KEY NOT NULL,
    bloss_begin_month integer NOT NULL, -- ok?
    bloss_begin_day integer,
    bloss_end_month integer NOT NULL,
    bloss_end_day integer
);

CREATE TABLE humidity_types (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
);

CREATE TABLE humidity_type_parts (
    id Serial PRIMARY KEY NOT NULL,
    humidity_type_id integer REFERENCES humidity_types(id) NOT NULL,
    geometry geometry
);

CREATE TABLE light_types (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
);

CREATE TABLE soil_acidity_types (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
);

CREATE TABLE soil_fertility_types (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
);

CREATE TABLE soil_types (
    id Serial PRIMARY KEY NOT NULL,
    -- acidity_type integer REFERENCES soil_acidity_types(id),
    -- fertility_type integer REFERENCES soil_fertility_types(id),
    name varchar UNIQUE NOT NULL
);

CREATE TABLE territories (
    id Serial PRIMARY KEY NOT NULL,
    type_id integer REFERENCES soil_types(id) NOT NULL,
    acidity_type_id integer REFERENCES soil_acidity_types(id) NOT NULL,
    fertility_type_id integer REFERENCES soil_fertility_types(id) NOT NULL,
    geometry geometry
);

CREATE TABLE limitation_factors (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL,
    explanation varchar NOT NULL
);

CREATE TABLE limitation_factor_parts (
    id Serial PRIMARY KEY NOT NULL,
    limitation_factor_id integer REFERENCES limitation_factors(id) NOT NULL,
    geometry geometry
);

CREATE TABLE features (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
);

CREATE TABLE climate_zones (
    id Serial PRIMARY KEY NOT NULL,
    usda_number integer NOT NULL,
    temperature_min integer NOT NULL,
    temperature_max integer NOT NULL,
    geometry geometry
);

-- references

CREATE TABLE plants (
    id Serial PRIMARY KEY NOT NULL,
    name_ru varchar UNIQUE NOT NULL,
    name_latin varchar UNIQUE NOT NULL,
    type integer REFERENCES plant_types(id),
    height_avg numeric(3, 1),
    crown_diameter numeric(3, 1),
    spread_aggressiveness_level integer,
    survivability_level integer,
    is_invasive boolean
);

CREATE TABLE plants_light_types (
    plant_id integer REFERENCES plants(id) NOT NULL,
    light_type_id integer REFERENCES light_types(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, light_type_id)
);

CREATE TABLE plants_soil_types (
    plant_id integer REFERENCES plants(id) NOT NULL,
    soil_type_id integer REFERENCES soil_types(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, soil_type_id)
);

CREATE TABLE plants_soil_acidity_types (
    plant_id integer REFERENCES plants(id) NOT NULL,
    soil_acidity_type_id integer REFERENCES soil_acidity_types(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, soil_acidity_type_id)
);

CREATE TABLE plants_soil_fertility_types (
    plant_id integer REFERENCES plants(id) NOT NULL,
    soil_fertility_type_id integer REFERENCES soil_fertility_types(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, soil_fertility_type_id)
);

CREATE TABLE plants_humidity_types (
    plant_id integer REFERENCES plants(id) NOT NULL,
    humidity_type_id integer REFERENCES humidity_types(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, humidity_type_id)
);

CREATE TABLE plants_features (
    plant_id integer REFERENCES plants(id) NOT NULL,
    feature_id integer REFERENCES features(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, feature_id)
);

CREATE TABLE plants_limitation_factors (
    plant_id integer REFERENCES plants(id) NOT NULL,
    limitation_factor_id integer REFERENCES limitation_factors(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, limitation_factor_id)
);

CREATE TABLE plants_climate_zones (
    plant_id integer REFERENCES plants(id) NOT NULL,
    climate_zone_id integer REFERENCES climate_zones(id) NOT NULL,
    is_stable boolean NOT NULL,
    PRIMARY KEY(plant_id, climate_zone_id)
);