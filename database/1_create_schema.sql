create extension postgis;

-- types

CREATE TYPE cohabitation_type AS ENUM ('negative', 'neutral', 'positive');

-- basics

CREATE TABLE plant_types (
    id Serial PRIMARY KEY NOT NULL,
    name varchar UNIQUE NOT NULL
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

CREATE TABLE light_type_parts (
    id Serial PRIMARY KEY NOT NULL,
    light_type_id integer REFERENCES light_types(id) NOT NULL,
    geometry geometry
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

CREATE TABLE genera (
    id Serial PRIMARY KEY NOT NULL,
    name_ru varchar(100) UNIQUE NOT NULL
);


-- references

CREATE TABLE cohabitation_comments (
    id Serial PRIMARY KEY NOT NULL,
    text varchar(250) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS cohabitation (
    genus_id_1 integer REFERENCES genera(id) NOT NULL,
    genus_id_2 integer REFERENCES genera(id) NOT NULL,
    cohabitation_type cohabitation_type NOT NULL,
    comment_id integer REFERENCES cohabitation_comments(id),
    PRIMARY KEY(genus_id_1, genus_id_2)
);

CREATE TABLE plants (
    id Serial PRIMARY KEY NOT NULL,
    name_ru varchar UNIQUE NOT NULL,
    name_latin varchar UNIQUE NOT NULL,
    type_id integer REFERENCES plant_types(id),
    height_avg numeric(3, 1),
    crown_diameter numeric(3, 1),
    spread_aggressiveness_level integer,
    survivability_level integer,
    is_invasive boolean,
    genus_id integer REFERENCES genera(id),
    photo_name varchar(256)
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

-- parks data

CREATE TABLE districts (
    id Serial PRIMARY KEY NOT NULL,
    name varchar(80) UNIQUE NOT NULL,
    sheet_name varchar(80) UNIQUE NOT NULL,
    geometry geometry
);

CREATE TABLE parks (
    id Serial PRIMARY KEY NOT NULL,
    district_id integer NOT NULL REFERENCES districts(id),
    name varchar(80) NOT NULL,
    geometry geometry,
    UNIQUE (district_id, name)
);

CREATE TABLE plants_parks (
    plant_id integer NOT NULL REFERENCES plants(id),
    park_id integer NOT NULL REFERENCES parks(id),
    PRIMARY KEY (plant_id, park_id)
);