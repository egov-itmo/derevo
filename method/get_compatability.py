import pandas as pd
import networkx as nx
import numpy as np
from data_collection import collect_plants_characteristics

def get_compatability_graph(database_link, return_gexf=False):
    '''
    returns compatability graph where weights of edges equals to outcome of species interaction 
    (1 for negative, 2 for neutral, 3 for positive)
    '''
    plants, x, y, cohabitation = collect_plants_characteristics(database_link) #drop x and y from func
    df_comp = plants.copy()
    df_comp = df_comp.join(df_comp, how='cross', rsuffix='_x')
    df_comp = df_comp[df_comp.name_ru != df_comp.name_ru_x]
    df_comp['genus_con'] = df_comp['genus_id'].astype(int).astype(str) + ':' + df_comp['genus_id_x'].astype(int).astype(str)
    cohabitation['genus_con'] = cohabitation['genus_id_1'].astype(str) + ':' + cohabitation['genus_id_2'].astype(str)
    df_comp = df_comp.merge(cohabitation[['cohabitation_type', 'genus_con']], on='genus_con', how='left')
    df_comp = (df_comp[~df_comp.filter(like='name_ru').apply(frozenset, axis=1).duplicated()].reset_index(drop=True))
    df_comp = df_comp.rename(columns={'cohabitation_type':'weight'})
    df_comp['weight'].fillna(2, inplace=True)
    df_comp['weight'].replace({'negative':1, 'neutral':2, 'positive':3}, inplace=True)
    df_comp = df_comp[['name_ru', 'name_ru_x', 'weight']]
    df_comp['is_compatability'] = 1
    compatability_graph = nx.from_pandas_edgelist(df_comp, 'name_ru', 'name_ru_x', 'weight', create_using=nx.MultiGraph(), edge_key = 'is_compatability')
    plant_dict = plants[['name_ru', 'name_latin', 'id', 'is_invasive', 'plant_type']]
    plant_dict['weights']= [', '.join([str(x) for x in list(np.sort(pd.unique(df_comp[df_comp.name_ru == species].weight)))]) for species in plants.name_ru]
    plant_dict.index = plant_dict.name_ru
    plant_dict = plant_dict.transpose()
    plant_dict = plant_dict[plant_dict.index != 'name_ru'].to_dict()
    nx.set_node_attributes(compatability_graph, plant_dict)
    if return_gexf == True:
        return nx.write_gexf(compatability_graph, "compatability_graph.gexf")
    else:
        return compatability_graph

def get_compatability_for_species(species_list, compatability_graph, return_gexf=False):
    '''
    returns compatability graph for a set of selected species
    '''
    current_graph = compatability_graph.subgraph(species_list)
    if return_gexf == True:
        nx.write_gexf(current_graph, "current_graph.gexf")
        print('Done')
        return
    else:
        return current_graph