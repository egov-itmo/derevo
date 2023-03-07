from sqlalchemy import create_engine
from .settings import engine_addr
from .data_collection import collect_plants_characteristics, collect_outer_factors, get_species_in_parks

engine = create_engine(engine_addr)
plants, plants_with_limitations_resistance, plants_suitable_for_light, cohabitation_attributes = collect_plants_characteristics()
species_in_parks = get_species_in_parks()
limitations, light = collect_outer_factors()