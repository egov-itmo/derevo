from sqlalchemy import create_engine
from .settings import engine_addr
from .data_collection import collect_plants_characteristics, collect_outer_factors, get_species_in_parks
from .get_composition import update_current_composition, get_recommended_composition, get_composition_unknown

engine = create_engine(engine_addr)
print('connected to the database')
plants, plants_with_limitations_resistance, plants_suitable_for_light, cohabitation_attributes = collect_plants_characteristics()
print('plant characteristic collected')
species_in_parks = get_species_in_parks()
print('plants in parks collected')
limitations, light = collect_outer_factors()
print('outer factors collected')