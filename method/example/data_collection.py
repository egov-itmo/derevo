"""
Data from database and OpenStreetMap collection logic is defined here.
"""
from typing import TextIO

import geopandas as gpd
import osm2geojson
import pandas as pd
import requests
from loguru import logger
from sqlalchemy import text
from sqlalchemy.engine import Connection

from derevo import Plant
from derevo import enumerations as c_enum

from .derevo_enums import EnumAdapters as c_adapt


def collect_plants(connection: Connection) -> list[Plant]:  # pylint: disable=too-many-locals
    """
    Collect plants from the database of a schema listed in backend part.
    """
    plants = []
    for (
        plant_id,
        name_ru,
        name_latin,
        genus_name,
        life_form_name,
        aggressiveness_level,
        survivability_level,
        is_invasive,
    ) in list(
        connection.execute(
            text(
                "SELECT"
                "   p.id,"
                "   p.name_ru,"
                "   p.name_latin,"
                "   g.name_ru,"
                "   t.name,"
                "   spread_aggressiveness_level,"
                "   survivability_level,"
                "   is_invasive"
                " FROM plants p"
                "   LEFT JOIN genera g ON p.genus_id = g.id"
                "   LEFT JOIN plant_types t ON p.type_id = t.id"
            )
        )
    ):
        life_form = c_adapt.life_forms.get(life_form_name)
        aggressiveness = c_adapt.aggressiveness_levels.get(aggressiveness_level)
        survivability = c_adapt.survivability_levels.get(survivability_level)

        res = connection.execute(
            text(
                "SELECT lf.name, is_stable"
                " FROM plants_limitation_factors p"
                "   JOIN limitation_factors lf ON p.limitation_factor_id = lf.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        limitation_factors_resistances = {
            c_adapt.limitation_factors[lf_name]: (
                c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL
            )
            for lf_name, is_stable in res
        }

        res = connection.execute(
            text(
                "SELECT usda.usda_number, is_stable"
                " FROM plants_climate_zones p"
                "   JOIN climate_zones usda ON p.climate_zone_id = usda.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        usda_zone_preferences = {
            c_enum.UsdaZone.from_value(usda_number): (
                c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL
            )
            for usda_number, is_stable in res
        }

        res = connection.execute(
            text(
                "SELECT lt.name, is_stable"
                " FROM plants_light_types p"
                "   JOIN light_types lt ON p.light_type_id = lt.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        light_preferences = {
            c_adapt.light[light_type_name]: (
                c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL
            )
            for light_type_name, is_stable in res
        }

        res = connection.execute(
            text(
                "SELECT ht.name, is_stable"
                " FROM plants_humidity_types p"
                "   JOIN humidity_types ht ON p.humidity_type_id = ht.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        humidity_preferences = {
            c_adapt.humidity[humidity_type_name]: (
                c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL
            )
            for humidity_type_name, is_stable in res
        }

        res = connection.execute(
            text(
                "SELECT at.name, is_stable"
                " FROM plants_soil_acidity_types p"
                "   JOIN soil_acidity_types at ON p.soil_acidity_type_id = at.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        soil_acidity_preferences = {
            c_adapt.acidity[acidity_type_name]: (
                c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL
            )
            for acidity_type_name, is_stable in res
        }

        res = connection.execute(
            text(
                "SELECT at.name, is_stable"
                " FROM plants_soil_fertility_types p"
                "   JOIN soil_fertility_types at ON p.soil_fertility_type_id = at.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        soil_fertility_preferences = {
            c_adapt.fertility[fertility_type_name]: (
                c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL
            )
            for fertility_type_name, is_stable in res
        }

        res = connection.execute(
            text(
                "SELECT at.name, is_stable"
                " FROM plants_soil_types p"
                "   JOIN soil_types at ON p.soil_type_id = at.id"
                " WHERE plant_id = :plant_id"
            ),
            {"plant_id": plant_id},
        )
        soil_type_preferences = {
            c_adapt.soil[type_name]: (c_enum.ToleranceType.POSITIVE if is_stable else c_enum.ToleranceType.NEUTRAL)
            for type_name, is_stable in res
        }

        plant = Plant(
            name_ru,
            name_latin,
            genus_name,
            life_form,
            limitation_factors_resistances,
            usda_zone_preferences,
            light_preferences,
            humidity_preferences,
            soil_acidity_preferences,
            soil_fertility_preferences,
            soil_type_preferences,
            aggressiveness,
            survivability,
            is_invasive,
        )
        plants.append(plant)
    return plants


def collect_plants_dataframe(connection: Connection) -> pd.DataFrame:
    """Get plants dataframe from database."""

    plants = pd.read_sql(
        text(
            "SELECT plants.id, plant_types.name AS plant_type, name_ru, name_latin,"
            "     spread_aggressiveness_level AS aggressiveness, survivability_level AS survivability,"
            "     is_invasive, genus_id"
            " FROM plants"
            "     JOIN plant_types ON plants.type_id = plant_types.id"
            " WHERE genus_id IS NOT NULL"
        ),
        con=connection,
    )

    return plants


def collect_plants_with_limitation_resistance(connection: Connection) -> pd.DataFrame:
    """Get plants with limitation factors dataframe from database."""

    plants_with_limitations_resistance = pd.read_sql(
        text(
            "SELECT p.id, pt.name AS plant_type, p.name_ru, p.name_latin,"
            "     p.spread_aggressiveness_level AS aggressiveness, p.survivability_level AS survivability,"
            "     p.is_invasive, p.genus_id, plf.limitation_factor_id, lf.name"
            " FROM plants p"
            "     JOIN plant_types pt ON p.type_id = pt.id"
            "     JOIN plants_limitation_factors plf ON plf.plant_id = p.id"
            "     JOIN limitation_factors lf ON lf.id = plf.limitation_factor_id"
            " WHERE plf.is_stable = true"
        ),
        con=connection,
    )

    return plants_with_limitations_resistance


def collect_plants_suitable_for_light(connection: Connection) -> pd.DataFrame:
    """Get plants with suitable light types dataframe from database."""

    plants_suitable_for_light = pd.read_sql(
        text(
            "SELECT p.id, pt.name AS plant_type, p.name_ru, p.name_latin,"
            "     p.spread_aggressiveness_level AS aggressiveness, p.survivability_level AS survivability,"
            "     p.is_invasive, p.genus_id, plt.light_type_id, lt.name"
            " FROM plants p"
            "     JOIN plant_types pt ON p.type_id = pt.id"
            "     JOIN plants_light_types plt ON plt.plant_id = p.id"
            "     JOIN light_types lt ON lt.id = plt.light_type_id"
            " WHERE plt.is_stable = true"
        ),
        con=connection,
    )

    return plants_suitable_for_light


def collect_cohabitations(connection: Connection) -> pd.DataFrame:
    """Get genera cohabitation dataframe from database."""

    cohabitation_attributes = pd.read_sql(
        text(
            "SELECT g1.name_ru as genus_name_1, g2.name_ru as genus_name_2, cohabitation_type"
            " FROM cohabitation c"
            "   JOIN genera g1 on c.genus_id_1 = g1.id"
            "   JOIN genera g2 on c.genus_id_2 = g2.id"
        ),
        con=connection,
    )

    return cohabitation_attributes


def collect_limitation_polygons(connection: Connection) -> gpd.GeoDataFrame:
    """Get GeoDataFrame with limitation polygons from database."""

    limitations = pd.read_sql(
        text("SELECT id, limitation_factor_id, ST_AsText(geometry) as geometry FROM limitation_factor_parts"),
        con=connection,
    )
    limitations["geometry"] = gpd.GeoSeries.from_wkt(limitations["geometry"])
    limitations = gpd.GeoDataFrame(limitations, geometry="geometry").set_crs(4326)

    return limitations


def collect_light_polygons(connection: Connection) -> gpd.GeoDataFrame:
    """Get GeoDataFrame with light polygons from database."""

    light = pd.read_sql(
        text("SELECT id, light_type_id, ST_AsText(geometry) as geometry FROM light_type_parts"),
        con=connection,
    )
    light["geometry"] = gpd.GeoSeries.from_wkt(light["geometry"])
    light = gpd.GeoDataFrame(light, geometry="geometry").set_crs(4326)

    return light


def collect_parks(path_to_green_areas_geojson: str | TextIO, target_parks: list[str] | None = None) -> gpd.GeoDataFrame:
    """
    Get dataframe of parks (green areas) read from file by name or a file-like object.

    Will be replaced with citygeotools integration in future verions.
    """
    parks = gpd.read_file(path_to_green_areas_geojson)
    if target_parks is not None:
        parks = parks[parks["service_name"].isin(target_parks)]
    return parks


def collect_species_in_parks(connection: Connection) -> pd.DataFrame:
    """Get plants in parks dataframe from database."""

    species_in_parks = pd.read_sql(
        text(
            "SELECT plants.id, name_ru, name as park_name"
            " FROM plants"
            "   JOIN plants_parks ON plants.id = plants_parks.plant_id"
            "   JOIN parks ON plants_parks.park_id = parks.id"
        ),
        con=connection,
    )
    return species_in_parks


def _cut_non_overlapping_parts(gdf):
    new_gdf = gdf.copy()
    spatial_index = gdf.sindex
    for idx, row in gdf.iterrows():
        geometry = row.geometry
        intersecting_indices = list(spatial_index.intersection(geometry.bounds))
        for idx2 in intersecting_indices:
            if idx == idx2:
                continue
            if geometry.intersects(gdf.iloc[idx2].geometry):
                geometry = geometry.intersection(gdf.iloc[idx2].geometry)
        new_gdf.at[idx, "geometry"] = geometry
    new_gdf = new_gdf[~new_gdf.geometry.is_empty]
    return new_gdf


def collect_smoke_area_from_osm(
    city: str,
    city_crs: int,
    overpass_url: str = "http://overpass-api.de/api/interpreter",
    upper_limit=40,
    lower_limit=10,
) -> gpd.GeoDataFrame:
    """_summary_

    Args:
        city (str): City name
        city_crs (int): City local coordinate system for correct buffer results in meters
        overpass_url (_type_, optional): URL to overpass-API whichsuits user the best.
        Defaults to "http://overpass-api.de/api/interpreter".
        upper_limit (int, optional): Number to multiply chimney height to create an outer buffer. Defaults to 40.
        lower_limit (int, optional): Number to multiply chinmey height to create an inner buffer. Defaults to 10.

    Returns:
        gpd.GeoDataFrame: _description_
    """

    overpass_query = f"""
    [out:json];
            area['name'='{city}']->.searchArea;
            (
                node["man_made"="chimney"](area.searchArea);
                way["man_made"="chimney"](area.searchArea);
                relation["man_made"="chimney"](area.searchArea);
            );
    out geom;
    """
    logger.debug("Performing overpass request for chimneys data")
    result = requests.get(overpass_url, params={"data": overpass_query}).json()  # pylint: disable=missing-timeout
    gdf = osm2geojson.json2geojson(result)
    gdf = gpd.GeoDataFrame.from_features(gdf["features"]).set_crs(4326).to_crs(city_crs)
    gdf = gdf[["geometry", "id", "tags"]]
    gdf.loc[gdf["geometry"].geom_type != "Point", "geometry"] = gdf["geometry"].centroid
    gdf = gdf.join(pd.json_normalize(gdf.tags)["height"]).drop(columns=["tags"])
    gdf["height"] = (
        gdf.height.fillna("10").map(lambda x: [char for char in x.split(" ") if char.isdigit()][0]).astype(int)
    )

    max_area = gdf.buffer(gdf.height * upper_limit)
    min_area = gdf.buffer(gdf.height * lower_limit)
    gdf["geometry"] = max_area.difference(min_area)
    gdf = _cut_non_overlapping_parts(gdf).dissolve().explode()
    gdf = gdf[gdf.area > 200].to_crs(4326)
    logger.debug("Got {} chimneys polygons", gdf.shape[0])

    return gdf
