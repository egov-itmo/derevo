import pandas as pd
import geopandas as gpd
import requests
import osm2geojson
import compositioner as cm

def collect_plants_characteristics(force_update=False):
    '''
    Collects dataframes with plants attributes from database.
    '''
    plants = pd.read_sql(
        f'''
        SELECT plants.id, plant_types.name AS plant_type, name_ru, name_latin,
            spread_aggressiveness_level AS aggressiveness, survivability_level AS survivability,
            is_invasive, genus_id
        FROM plants
        JOIN plant_types ON plants.type_id = plant_types.id
        ''', 
        con=cm.engine
    )

    plants = plants.dropna(subset=['genus_id'])

    plants_limitations = pd.read_sql(
        '''
        SELECT * FROM plants_limitation_factors WHERE is_stable = True
        ''', 
        con=cm.engine
    )

    plants_light = pd.read_sql(
        '''
        SELECT * FROM plants_light_types WHERE is_stable = True
        ''', 
        con=cm.engine
    )

    plants_with_limitations_resistance = plants.merge(
        plants_limitations,
        left_on='id',
        right_on='plant_id',
        how='inner'
    )

    plants_suitable_for_light = plants.merge(
        plants_light,
        left_on='id',
        right_on='plant_id',
        how='inner'
    )

    cohabitation_attributes = pd.read_sql(
        '''
        SELECT * FROM cohabitation
        ''', 
        con=cm.engine
    )

    if force_update:
        cm.plants = plants
        cm.plants_with_limitations_resistance = plants_with_limitations_resistance
        cm.plants_suitable_for_light = plants_suitable_for_light
        cm.cohabitation_attributes = cohabitation_attributes
        print('Variables updated.')
        return
    else:
        return plants, plants_with_limitations_resistance, plants_suitable_for_light, cohabitation_attributes

def collect_outer_factors(force_update=False):
    """Collects polygons with outer factors (light and limitations) from database."""
    limitations = pd.read_sql(
        """
        SELECT id, limitation_factor_id, ST_AsText(geometry) as geometry 
        FROM limitation_factor_parts
        """,
        con=cm.engine
    )
    limitations["geometry"] = gpd.GeoSeries.from_wkt(limitations["geometry"])
    limitations = gpd.GeoDataFrame(limitations, geometry="geometry").set_crs(4326)

    light = pd.read_sql(
        """
        SELECT id, light_type_id, ST_AsText(geometry) as geometry 
        FROM light_type_parts
        """,
        con=cm.engine
    )
    light["geometry"] = gpd.GeoSeries.from_wkt(light["geometry"])
    light = gpd.GeoDataFrame(light, geometry="geometry").set_crs(4326)

    if force_update:
        cm.limitations = limitations
        cm.light = light
        print("Spatial variables updated.")
        return
    else:
        return limitations, light

def get_polygons(path_to_polygons, target_parks=None):
    """Returns polygons of green areas, temporary, will be replaced with citygeotools integration."""
    parks = gpd.read_file(path_to_polygons)
    if target_parks is not None:
        parks = parks[parks.service_name.isin(target_parks)]
    return parks


def get_species_in_parks(force_update=False):
    """Gets species in parks."""
    species_in_parks = pd.read_sql(
        f"""
        SELECT plants.id, name_ru, name as park_name
        FROM plants
        JOIN plants_parks ON plants.id = plants_parks.plant_id 
        JOIN parks ON plants_parks.park_id = parks.id
        """,
        con=cm.engine
    )
    if force_update:
        cm.species_in_parks = species_in_parks
        print("Species in parks updated.")
        return
    else:
        return species_in_parks
    
def get_smoke_area(city, city_crs):
    UPPER_LIMIT = 40
    LOWER_LIMIT = 10

    overpass_url = "http://overpass-api.de/api/interpreter"
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
    result = requests.get(overpass_url, params={'data': overpass_query}).json()
    gdf = osm2geojson.json2geojson(result)
    gdf = gpd.GeoDataFrame.from_features(gdf["features"]).set_crs(4326).to_crs(city_crs)
    gdf = gdf[["geometry", "id", "tags"]]
    gdf.loc[gdf['geometry'].geom_type != 'Point', 'geometry'] = gdf['geometry'].centroid
    gdf = gdf.join(pd.json_normalize(gdf.tags)['height']).drop(columns=['tags'])
    gdf['height'] = gdf.height.fillna('10').map(lambda x: [char for char in x.split(' ') if char.isdigit()][0]).astype(int)

    max_area = gdf.buffer(gdf.height * UPPER_LIMIT)
    min_area = gdf.buffer(gdf.height * LOWER_LIMIT)
    gdf['geometry'] = max_area.difference(min_area).to_crs(4326)

    return gdf
