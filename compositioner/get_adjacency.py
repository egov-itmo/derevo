import pandas as pd
import networkx as nx
import compositioner as cm


def get_adjacency_graph(edge_key_value=1, target_parks=None, return_gexf=False, output_path='adjacency_graph'):
    """
    Returns adjacency graph where weight of edges equals to number of co-occurrence cases.
    """
    species_in_locations = cm.species_in_parks.copy()

    if target_parks is not None:
        species_in_locations = species_in_locations[species_in_locations['park_name'].isin(target_parks)]

    loc_list = list(pd.unique(species_in_locations['park_name']))
    species_total = []

    for loc in loc_list:
        local_species = species_in_locations[species_in_locations['park_name'] == loc]
        local_species = local_species.join(local_species['name_ru'], how='cross', rsuffix='_x')
        local_species = local_species[local_species['name_ru'] != local_species['name_ru_x']]
        local_species['edge'] = local_species['name_ru'] + ':' + local_species['name_ru_x']
        species_total.append(local_species)

    species_total = pd.concat(species_total)
    df_comp = species_total.groupby('edge').count()['park_name'].reset_index()
    df_comp[['name_ru', 'name_ru_x']] = df_comp['edge'].str.split(':', 1, expand=True)
    df_comp = (df_comp[~df_comp.filter(like='name_ru').apply(frozenset, axis=1).duplicated()]
               .reset_index(drop=True))
    df_comp.rename(columns={'park_name': 'weight'}, inplace=True)
    df_comp = df_comp[['name_ru', 'name_ru_x', 'weight']]
    df_comp['is_compatibility'] = edge_key_value

    current_graph = nx.from_pandas_edgelist(df_comp, 'name_ru', 'name_ru_x', 'weight',
                                            create_using=nx.MultiGraph(), edge_key='is_compatibility')

    if return_gexf:
        nx.write_gexf(current_graph, f"{output_path}.gexf")
    else:
        return current_graph
