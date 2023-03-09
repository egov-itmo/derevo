import compositioner as cm

def update_variables():
    cm.plants, cm.plants_with_limitations_resistance, cm.plants_suitable_for_light,\
         cm.cohabitation_attributes = cm.collect_plants_characteristics(force_update=True)
    cm.limitations, cm.light = cm.collect_outer_factors(force_update=True)
    return