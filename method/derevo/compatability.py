"""
Get cohabitation graph method is defined here
"""
from __future__ import annotations

from typing import BinaryIO

import networkx as nx
import numpy as np
import pandas as pd


def get_compatability_graph(
    plants: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
) -> nx.Graph:
    """
    Return compatability graph where weights of edges equals to outcome of species interaction
    (1 for negative, 2 for neutral, 3 for positive).
    """
    plants = plants.copy()
    cohabitation = cohabitation_attributes.copy()
    df_comp = plants.copy()
    df_comp = df_comp.join(df_comp, how="cross", rsuffix="_x")
    df_comp = df_comp[df_comp["name_ru"] != df_comp["name_ru_x"]]
    df_comp["genus_con"] = df_comp["genus"] + ":" + df_comp["genus_x"]
    cohabitation["genus_con"] = cohabitation["genus_name_1"] + ":" + cohabitation["genus_name_2"]
    df_comp = df_comp.merge(cohabitation[["cohabitation_type", "genus_con"]], on="genus_con", how="left")
    df_comp = df_comp[~df_comp.filter(like="name_ru").apply(frozenset, axis=1).duplicated()].reset_index(drop=True)
    df_comp = df_comp.rename(columns={"cohabitation_type": "weight"})
    df_comp["weight"].fillna(2, inplace=True)
    # df_comp["weight"].replace({"negative": 1, "neutral": 2, "positive": 3}, inplace=True)
    df_comp["weight"].replace({"negative": -1, "neutral": 0, "positive": 1}, inplace=True)
    df_comp = df_comp[["name_ru", "name_ru_x", "weight"]]
    df_comp["is_compatability"] = 1
    compatability_graph = nx.from_pandas_edgelist(
        df_comp,
        "name_ru",
        "name_ru_x",
        "weight",
        create_using=nx.MultiGraph(),
        edge_key="is_compatability",
    )
    plant_dict = plants[["name_ru", "name_latin", "is_invasive", "life_form"]].copy()
    plant_dict["weights"] = [
        ", ".join(
            [
                str(x)
                for x in list(
                    np.sort(df_comp[df_comp["name_ru"] == species]["weight"].unique()),
                )
            ]
        )
        for species in plants["name_ru"]
    ]
    plant_dict.index = plant_dict["name_ru"]
    plant_dict = plant_dict.transpose()
    plant_dict = plant_dict[plant_dict.index != "name_ru"].to_dict()
    nx.set_node_attributes(compatability_graph, plant_dict)

    return compatability_graph


def write_compatability_graph_gexf(
    plants: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    output_path: str | BinaryIO = "compatability_graph.gexf",
) -> None:
    """
    Write compatability graph where weights of edges equals to outcome of species interaction
    (1 for negative, 2 for neutral, 3 for positive) to a given file (by name or a binary file-like object)
    in gexf format.
    """
    compatability_graph = get_compatability_graph(plants, cohabitation_attributes)
    nx.write_gexf(compatability_graph, f"{output_path}.gexf")


def get_compatability_for_species(
    species_list: list[str],
    compatability_graph,
) -> nx.Graph:
    """
    Return compatability graph for a set of selected species.
    """
    current_graph = compatability_graph.subgraph(species_list)
    return current_graph


def write_compatability_for_species_gexf(
    species_list: list[str],
    compatability_graph,
    output_path: str | BinaryIO = "compatability_graph.gexf",
) -> None:
    """
    Return compatability graph for a set of selected species.
    """
    current_graph = get_compatability_graph(species_list, compatability_graph)
    nx.write_gexf(current_graph, output_path)
