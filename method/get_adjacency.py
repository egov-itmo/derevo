import pandas as pd
import networkx as nx

def get_existing_species(locations, target_parks=None):
    '''
    returns dataframe with species, parks and districts, green_base.xlsx will be added to the database
    '''
    species_in_locations = []
    for loc in locations:
        df_green = pd.read_excel('landscaping/database/green_base.xlsx', sheet_name=loc)
        df_green = pd.melt(df_green)
        df_green['district'] = loc
        species_in_locations.append(df_green)
    species_in_locations = pd.concat(species_in_locations).dropna()
    species_in_locations.rename(columns={'variable':'park_name', 'value':'species'}, inplace=True)
    species_in_locations = species_in_locations[species_in_locations.park_name != ' ']
    species_in_locations['park_name'] = species_in_locations.park_name.str.replace('\\n', '')
    if target_parks != None:
        species_in_locations = species_in_locations[species_in_locations.park_name.isin(target_parks)]
    return species_in_locations

def get_adjacency_graph(locations, target_parks=None, return_gexf=False):
    '''
    returns adjacency graph where weight of edges equals to number of co-occurence cases
    '''
    species_in_locations = get_existing_species(locations, target_parks)
    loc_list = list(pd.unique(species_in_locations.park_name))
    species_total = []
    for loc in loc_list:
        local_species = species_in_locations[species_in_locations.park_name == loc]
        local_species = local_species.join(local_species.species, how='cross', rsuffix='_x')
        local_species = local_species[local_species.species != local_species.species_x]
        local_species['edge'] = local_species.species + ':' + local_species.species_x
        species_total.append(local_species)
    species_total = pd.concat(species_total)
    df_comp = species_total.groupby('edge').count()['park_name'].reset_index()
    df_comp[['name_ru', 'name_ru_x']] = df_comp.edge.str.split(':', 1, expand=True)
    df_comp = (df_comp[~df_comp.filter(like='name_ru').apply(frozenset, axis=1).duplicated()]
        .reset_index(drop=True))
    df_comp.rename(columns={'park_name':'weight'}, inplace=True)
    df_comp = df_comp[['name_ru', 'name_ru_x', 'weight']]
    #df_comp['is_compatability'] = 0
    df_comp['is_compatability'] = 1
    current_graph = nx.from_pandas_edgelist(df_comp, 'name_ru', 'name_ru_x', 'weight',
    create_using=nx.MultiGraph(), edge_key = 'is_compatability')
    if return_gexf == True:
        return nx.write_gexf(current_graph, "adjacency_graph.gexf")
    else:
        return current_graph
