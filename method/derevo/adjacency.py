"""
Get adjency graph method is defined here.
"""
from __future__ import annotations

from typing import BinaryIO

import networkx as nx
import pandas as pd


def get_adjacency_graph(
    species_in_parks: pd.DataFrame,
    edge_key_value: int = 1,
    target_parks: list[str] | None = None,
) -> nx.Graph:
    """
    Return adjacency graph where weight of edges equals to number of co-occurence cases.
    """
    species_in_locations = species_in_parks.copy()
    if target_parks is not None:
        species_in_locations = species_in_locations[species_in_locations["park_name"].isin(target_parks)]
    loc_list: list[str] = list(species_in_locations["park_name"].unique())
    species_total = []
    for loc in loc_list:
        local_species: pd.DataFrame = species_in_locations[species_in_locations["park_name"] == loc]
        local_species = local_species.join(local_species["name_ru"], how="cross", rsuffix="_x")
        local_species = local_species[local_species["name_ru"] != local_species["name_ru_x"]]
        local_species["edge"] = local_species["name_ru"] + ":" + local_species["name_ru_x"]
        species_total.append(local_species)
    species_total = pd.concat(species_total)
    df_comp: pd.DataFrame = species_total.groupby("edge").count()["park_name"].reset_index()
    df_comp[["name_ru", "name_ru_x"]] = df_comp["edge"].str.split(":", 1, expand=True)
    df_comp = df_comp[~df_comp.filter(like="name_ru").apply(frozenset, axis=1).duplicated()].reset_index(drop=True)
    df_comp.rename(columns={"park_name": "weight"}, inplace=True)
    df_comp = df_comp[["name_ru", "name_ru_x", "weight"]]
    df_comp["is_compatability"] = edge_key_value
    current_graph = nx.from_pandas_edgelist(
        df_comp,
        "name_ru",
        "name_ru_x",
        "weight",
        create_using=nx.MultiGraph(),
        edge_key="is_compatability",
    )
    return current_graph


def write_adjacency_graph_gexf(
    species_in_parks: pd.DataFrame,
    output_path: str | BinaryIO = "adjacency_graph.gexf",
    edge_key_value: int = 1,
    target_parks: list[str] | None = None,
) -> None:
    """
    Write adjacency graph where weight of edges equals to number of co-occurence cases
    to a given file (by name or a binary file-like object) in gexf format.
    """
    current_graph = get_adjacency_graph(species_in_parks, edge_key_value, target_parks)
    nx.write_gexf(current_graph, output_path)
