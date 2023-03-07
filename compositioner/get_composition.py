import pandas as pd
import geopandas as gpd
import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities
import compositioner as cm
from compositioner.get_compatability import get_compatability_graph
from compositioner.get_adjacency import get_adjacency_graph

def _intersection_check(input, factor):
    '''
    utility function to determine if greenery polygon intersects with another polygon of light or limitation factor
    '''
    for i in factor.index:
        if input.intersects(factor.loc[i].geometry) == True:
            return True
    return False

def get_species_composition_old(greenery_polygon):
    '''
    needs refactoring; returns Series with strings with composition of plants
    '''
    plants = cm.plants.copy()
    plants_with_lim_resist = cm.plants_with_limitations_resistance.copy()
    plants_with_lig_resist = cm.plants_suitable_for_light.copy()
    cohabitation = cm.cohabitation_attributes.copy()
    limitations = cm.limitations.copy()
    light = cm.light.copy()
    #finding species which can grow in existing light conditions
    light_types = list(pd.unique(light.light_type_id))
    lig_list = [lig_id for lig_id in light_types if _intersection_check(greenery_polygon, light.query(f'light_type_id == {lig_id}'))]
    filtered_plants = plants_with_lig_resist[plants_with_lig_resist.light_type_id.isin(lig_list)]
    light_comp = list(pd.unique(filtered_plants.name_ru))
    print('number of light conditions:', len(lig_list))
    #finding species which can grow with existing limitations
    limitation_factors = list(pd.unique(limitations.limitation_factor_id))
    lim_list = [lim_id for lim_id in limitation_factors if _intersection_check(greenery_polygon, limitations.query(f'limitation_factor_id == {lim_id}'))]
    filtered_plants = plants_with_lim_resist[plants_with_lim_resist.limitation_factor_id.isin(lim_list)]
    limitations_comp = filtered_plants.groupby('name_ru').count().reset_index()
    limitations_comp = limitations_comp[limitations_comp.limitation_factor_id == limitations_comp.limitation_factor_id.max()]
    limitations_comp = list(pd.unique(limitations_comp.name_ru))
    print('Number of limitation factors:', len(lim_list))
    #filtering species by environmental factors
    if len(lig_list) > 0:
        df_comp = plants[plants.name_ru.isin(light_comp)]
    else:
        print('No light conditions')
        return None
    if len(lim_list) > 0:
        df_comp = df_comp[df_comp.name_ru.isin(limitations_comp)]
    else:
        df_comp = df_comp
    #connecting with cohabitation weights
    edge_1 = df_comp.merge(cohabitation, left_on = 'genus_id', right_on='genus_id_1', how='left')
    edge_1.dropna(subset='genus_id_1', inplace=True)
    edge_2 = edge_1.merge(df_comp, left_on='genus_id_2', right_on='genus_id', how='left').\
        rename(columns={'name_ru_x':'u', 'name_ru_y':'v'})[['u', 'v', 'cohabitation_type']]
    edge_2.dropna(inplace=True)
    edge_2 = edge_2.rename(columns={'cohabitation_type':'weight'})
    edge_2['weight'].replace({'negative':1, 'neutral':2, 'positive':3}, inplace=True)
    #creating graph and finding biggest community
    green_graph = nx.from_pandas_edgelist(edge_2, 'u', 'v', 'weight')
    communities_list = greedy_modularity_communities(green_graph, weight='weight')
    size_of_biggest_community = max([len(com) for com in communities_list])
    print('biggest community has', size_of_biggest_community, 'members')
    composition = ', '.join([', '.join(com) for com in communities_list if len(com) == size_of_biggest_community])
    return composition

def update_current_composition(greenery_polygon, locations, target_parks, return_gexf=False, output_path = 'updated_graph'):
    '''
    returns list of graphs with variants of updated plants composition
    '''
    #version with all edges
    plants = cm.plants.copy()
    plants_with_lim_resist = cm.plants_with_limitations_resistance.copy()
    plants_with_lig_resist = cm.plants_suitable_for_light.copy()
    limitations = cm.limitations.copy()
    light = cm.light.copy()
    #finding species which can grow in existing light conditions
    light_types = list(pd.unique(light.light_type_id))
    lig_list = [lig_id for lig_id in light_types if _intersection_check(greenery_polygon, light.query(f'light_type_id == {lig_id}'))]
    filtered_plants = plants_with_lig_resist[plants_with_lig_resist.light_type_id.isin(lig_list)]
    light_comp = list(pd.unique(filtered_plants.name_ru))
    print('number of light conditions:', len(lig_list))
    #finding species which can grow with existing limitations
    limitation_factors = list(pd.unique(limitations.limitation_factor_id))
    lim_list = [lim_id for lim_id in limitation_factors if _intersection_check(greenery_polygon, limitations.query(f'limitation_factor_id == {lim_id}'))]
    filtered_plants = plants_with_lim_resist[plants_with_lim_resist.limitation_factor_id.isin(lim_list)]
    limitations_comp = filtered_plants.groupby('name_ru').count().reset_index()
    limitations_comp = limitations_comp[limitations_comp.limitation_factor_id == limitations_comp.limitation_factor_id.max()]
    limitations_comp = list(pd.unique(limitations_comp.name_ru))
    print('Number of limitation factors:', len(lim_list))
    #filtering species by environmental factors
    if len(lig_list) > 0:
        df_comp = plants[plants.name_ru.isin(light_comp)]
    else:
        print('No light conditions')
        return None
    if len(lim_list) > 0:
        df_comp = df_comp[df_comp.name_ru.isin(limitations_comp)]
    else:
        df_comp = df_comp
    
    compatability_graph = get_compatability_graph()
    comp_graph = compatability_graph.copy()
    comp_graph = comp_graph.subgraph(df_comp.name_ru)
    communities_list = greedy_modularity_communities(comp_graph, weight='weight')
    print(len(communities_list), 'communities here')
        
    compositions = [list(com) for com in communities_list]
    current_graph = get_adjacency_graph(locations, target_parks)
    current_composition = list(nx.to_pandas_edgelist(current_graph).source.unique())
    
    graph_variants = []
    for composition in compositions:
        upd_comp = composition + current_composition
        updated_graph = compatability_graph.subgraph(upd_comp)
        for node_id in composition:
            updated_graph.nodes[node_id]['is_added'] = True
        for node_id in current_composition:
            updated_graph.nodes[node_id]['is_added'] = False
        graph_variants.append(updated_graph)

    if return_gexf == True:
        for graph in graph_variants:
            nx.write_gexf(graph, f"{output_path}_v_{graph_variants.index(graph)}.gexf")
        print('Done')
        return
    else:
        return graph_variants

def get_recommended_composition(greenery_polygon, database_link, return_gexf=False, output_path = 'recommended_graph'):
    '''
    returns list of graphs with variants of recommended composition with account for outer factors
    '''
    plants = cm.plants.copy()
    plants_with_lim_resist = cm.plants_with_limitations_resistance.copy()
    plants_with_lig_resist = cm.plants_suitable_for_light.copy()
    limitations = cm.limitations.copy()
    light = cm.light.copy()
    #finding species which can grow in existing light conditions
    light_types = list(pd.unique(light.light_type_id))
    lig_list = [lig_id for lig_id in light_types if _intersection_check(greenery_polygon, light.query(f'light_type_id == {lig_id}'))]
    filtered_plants = plants_with_lig_resist[plants_with_lig_resist.light_type_id.isin(lig_list)]
    light_comp = list(pd.unique(filtered_plants.name_ru))
    print('number of light conditions:', len(lig_list))
    #finding species which can grow with existing limitations
    limitation_factors = list(pd.unique(limitations.limitation_factor_id))
    lim_list = [lim_id for lim_id in limitation_factors if _intersection_check(greenery_polygon, limitations.query(f'limitation_factor_id == {lim_id}'))]
    filtered_plants = plants_with_lim_resist[plants_with_lim_resist.limitation_factor_id.isin(lim_list)]
    limitations_comp = filtered_plants.groupby('name_ru').count().reset_index()
    limitations_comp = limitations_comp[limitations_comp.limitation_factor_id == limitations_comp.limitation_factor_id.max()]
    limitations_comp = list(pd.unique(limitations_comp.name_ru))
    print('Number of limitation factors:', len(lim_list))
    #filtering species by environmental factors
    if len(lig_list) > 0:
        df_comp = plants[plants.name_ru.isin(light_comp)]
    else:
        print('No light conditions')
        return None
    if len(lim_list) > 0:
        df_comp = df_comp[df_comp.name_ru.isin(limitations_comp)]
    else:
        df_comp = df_comp
    
    compatability_graph = get_compatability_graph(database_link)
    comp_graph = compatability_graph.copy()
    comp_graph = comp_graph.subgraph(df_comp.name_ru)
    communities_list = greedy_modularity_communities(comp_graph, weight='weight')
    print(len(communities_list), 'communities here')
        
    compositions = [list(com) for com in communities_list]
    graph_variants = []
    for composition in compositions:
        recommended_graph = compatability_graph.subgraph(composition)
        for node_id in composition:
            recommended_graph.nodes[node_id]['is_added'] = True
        graph_variants.append(recommended_graph)

    if return_gexf == True:
        for graph in graph_variants:
           nx.write_gexf(graph, f"{output_path}_v_{graph_variants.index(graph)}.gexf") 
        print('Done')
        return
    else:
        return graph_variants

def get_composition_unknown(return_gexf=False, output_path = 'new_graph'):
    '''
    returns list of graphs with variants of recommended composition for a place with unknown outer factors
    '''
    compatability_graph = get_compatability_graph()
    communities_list = greedy_modularity_communities(compatability_graph, weight='weight')
    print(len(communities_list), 'communities here')
    compositions = [list(com) for com in communities_list]
    graph_variants = []
    for composition in compositions:
        recommended_graph = compatability_graph.subgraph(composition)
        for node_id in composition:
            recommended_graph.nodes[node_id]['is_added'] = True
        recommended_graph.nodes.data('is_added', default=False)
        graph_variants.append(recommended_graph)
    if return_gexf:
        for graph in graph_variants:
            nx.write_gexf(graph, f"{output_path}_v_{graph_variants.index(graph)}.gexf")
        print('Done')
        return
    else:
        return graph_variants

