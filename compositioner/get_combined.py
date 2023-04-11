import networkx as nx
import compositioner as cm
from compositioner.get_adjacency import get_adjacency_graph


def get_combined_graph(target_parks=None, return_gexf=False, output_path='combined_graph'):
    '''
    Returns combined graph with weights equal to number of co-occurence cases and compatability outcome in attributes.
    '''
    plants = cm.plants.copy()
    cohabitation = cm.cohabitation_attributes.copy()

    # Create compatibility dataframe
    df_comp = plants.copy()
    df_comp = df_comp.join(df_comp, how='cross', rsuffix='_x')
    df_comp = df_comp[df_comp.name_ru != df_comp.name_ru_x]
    df_comp['genus_con'] = df_comp['genus_id'].astype(int).astype(str) + ':' + df_comp['genus_id_x'].astype(int).astype(str)
    cohabitation['genus_con'] = cohabitation['genus_id_1'].astype(str) + ':' + cohabitation['genus_id_2'].astype(str)
    df_comp = df_comp.merge(cohabitation[['cohabitation_type', 'genus_con']], on='genus_con', how='left')
    df_comp = df_comp[~df_comp.filter(like='name_ru').apply(frozenset, axis=1).duplicated()].reset_index(drop=True)
    df_comp['cohabitation_type'].fillna('neutral', inplace=True)
    df_comp = df_comp[['name_ru', 'name_ru_x', 'cohabitation_type']]
    df_comp['is_compatability'] = 1

    # Create adjacency dataframe
    df_adjacency = nx.to_pandas_edgelist(get_adjacency_graph(target_parks=target_parks))

    # Combine compatibility and adjacency dataframes
    df_comp = df_comp.rename(columns={'name_ru': 'source', 'name_ru_x': 'target'}) \
        .merge(df_adjacency[['source', 'target', 'weight']], on=['source', 'target'], how='left')
    if target_parks is not None:
        df_comp = df_comp[df_comp['source'].isin(df_adjacency['source'].unique())]
    df_comp = df_comp.fillna(0.1)
    df_comp.loc[df_comp.weight != 0.1, 'cohabitation_type'] = 'has_cases'

    # Create combined graph
    combined_graph = nx.from_pandas_edgelist(df_comp, 'source', 'target', ['weight', 'cohabitation_type'],
                                             create_using=nx.MultiGraph(), edge_key='is_compatability')
    plant_dict = plants[['name_ru', 'name_latin', 'id', 'is_invasive', 'plant_type']]
    plant_dict.index = plant_dict.name_ru
    plant_dict = plant_dict.transpose()
    plant_dict = plant_dict[plant_dict.index != 'name_ru'].to_dict()
    nx.set_node_attributes(combined_graph, plant_dict)

    # Return or save combined graph
    if return_gexf:
        nx.write_gexf(combined_graph, f"{output_path}.gexf")
        print('Done')
        return
    else:
        return combined_graph
