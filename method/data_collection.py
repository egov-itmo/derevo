import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine

def collect_plants_characteristics(database_link):
    '''
    collects dataframes with plants attributes from database
    '''
    engine = create_engine(database_link)
    plants = pd.read_sql(f'''SELECT plants.id, plant_types.name as plant_type, name_ru, name_latin, spread_aggressiveness_level as aggressivness, survivability_level as survivability, is_invasive, genus_id
                        FROM plants JOIN plant_types ON plants.type_id=plant_types.id''', con=engine)
    plants = plants.dropna(subset='genus_id')
    plants_limitations = pd.read_sql(f'''SELECT * FROM plants_limitation_factors WHERE is_stable = True''', con=engine)
    plants_light = pd.read_sql(f'''SELECT * FROM plants_light_types WHERE is_stable = True''', con=engine)
    plants_with_limitations_resistance = plants.merge(plants_limitations, left_on='id', right_on='plant_id', how='inner')
    plants_suitable_for_light = plants.merge(plants_light, left_on='id', right_on='plant_id', how='inner')
    cohabitation_attributes = pd.read_sql('''SELECT * FROM cohabitation''', con=engine)
    return plants, plants_with_limitations_resistance, plants_suitable_for_light, cohabitation_attributes

def collect_outer_factors(database_link):
    '''
    collects polygons with outer factors (light and limitations) from database
    '''
    engine = create_engine(database_link)
    limitations = pd.read_sql('''SELECT id, limitation_factor_id, ST_AsText(geometry) as geometry 
                            FROM limitation_factor_parts''', con=engine)
    limitations['geometry'] = gpd.GeoSeries.from_wkt(limitations['geometry'])
    limitations = gpd.GeoDataFrame(limitations, geometry='geometry').set_crs(4326)

    light = pd.read_sql('''SELECT id, light_type_id, ST_AsText(geometry) as geometry 
                            FROM light_types_parts''', con=engine)
    light['geometry'] = gpd.GeoSeries.from_wkt(light['geometry'])
    light = gpd.GeoDataFrame(light, geometry='geometry').set_crs(4326)
    return limitations, light

def get_polygons(target_parks=None):
    '''
    returns polygons of green areas, temporary, will be replaced with citygeotools integration
    '''
    parks = gpd.read_file('landscaping/method/parks.geojson')
    if target_parks != None:
        parks = parks[parks.service_name.isin(target_parks)]
    return parks