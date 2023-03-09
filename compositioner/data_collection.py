import pandas as pd
import geopandas as gpd
import compositioner as cm

def collect_plants_characteristics(force_update = False):
    '''
    collects dataframes with plants attributes from database
    '''
    plants = pd.read_sql(f'''SELECT plants.id, plant_types.name as plant_type, name_ru, name_latin, spread_aggressiveness_level as aggressivness, survivability_level as survivability, is_invasive, genus_id
                        FROM plants JOIN plant_types ON plants.type_id=plant_types.id''', con=cm.engine)
    plants = plants.dropna(subset=['genus_id'])
    plants_limitations = pd.read_sql(f'''SELECT * FROM plants_limitation_factors WHERE is_stable = True''', con=cm.engine)
    plants_light = pd.read_sql(f'''SELECT * FROM plants_light_types WHERE is_stable = True''', con=cm.engine)
    plants_with_limitations_resistance = plants.merge(plants_limitations, left_on='id', right_on='plant_id', how='inner')
    plants_suitable_for_light = plants.merge(plants_light, left_on='id', right_on='plant_id', how='inner')
    cohabitation_attributes = pd.read_sql('''SELECT * FROM cohabitation''', con=cm.engine)
    if force_update:
        cm.plants = plants
        cm.plants_with_limitations_resistance = plants_with_limitations_resistance
        cm.plants_suitable_for_light = plants_suitable_for_light
        cm.cohabitation_attributes = cohabitation_attributes
        print('variables updated')
        return
    else:
        return plants, plants_with_limitations_resistance, plants_suitable_for_light, cohabitation_attributes

def collect_outer_factors(force_update = False):
    '''
    collects polygons with outer factors (light and limitations) from database
    '''
    limitations = pd.read_sql('''SELECT id, limitation_factor_id, ST_AsText(geometry) as geometry 
                            FROM limitation_factor_parts''', con=cm.engine)
    limitations['geometry'] = gpd.GeoSeries.from_wkt(limitations['geometry'])
    limitations = gpd.GeoDataFrame(limitations, geometry='geometry').set_crs(4326)

    light = pd.read_sql('''SELECT id, light_type_id, ST_AsText(geometry) as geometry 
                            FROM light_type_parts''', con=cm.engine)
    light['geometry'] = gpd.GeoSeries.from_wkt(light['geometry'])
    light = gpd.GeoDataFrame(light, geometry='geometry').set_crs(4326)
    if force_update:
        cm.limitations = limitations
        cm.light = light
        print('spatial variables updated')
        return
    else:
        return limitations, light

def get_polygons(path_to_polygons, target_parks=None):
    '''
    returns polygons of green areas, temporary, will be replaced with citygeotools integration
    '''
    parks = gpd.read_file(path_to_polygons)
    if target_parks is not None:
        parks = parks[parks.service_name.isin(target_parks)]
    return parks

def get_species_in_parks(force_update = False):
    species_in_parks = pd.read_sql(f'''SELECT plants.id, name_ru, name as park_name
                        FROM plants JOIN plants_parks ON plants.id=plants_parks.plant_id 
                        JOIN parks ON plants_parks.park_id=parks.id''', con=cm.engine)
    if force_update:
        cm.species_in_parks = species_in_parks
        print('species in parks updated')
        return
    else:
        return species_in_parks