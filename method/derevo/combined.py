"""
Get combined graph method is defined here.
"""
from io import BytesIO
import networkx as nx
import pandas as pd

from derevo.adjacency import get_adjacency_graph


def get_combined_graph(
    plants: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    species_in_parks: pd.DataFrame,
    target_parks: list[str] | None = None,
) -> nx.Graph:
    """
    Returns combined graph with weights equal to number of co-occurence cases and compatability outcome in attributes.
    """
    plants = plants.copy()
    cohabitation = cohabitation_attributes.copy()
    df_comp = plants.copy()
    df_comp = df_comp.join(df_comp, how="cross", rsuffix="_x")
    df_comp = df_comp[df_comp.name_ru != df_comp.name_ru_x]
    df_comp["genus_con"] = (
        df_comp["genus_id"].astype(int).astype(str) + ":" + df_comp["genus_id_x"].astype(int).astype(str)
    )
    cohabitation["genus_con"] = cohabitation["genus_id_1"].astype(str) + ":" + cohabitation["genus_id_2"].astype(str)
    df_comp = df_comp.merge(cohabitation[["cohabitation_type", "genus_con"]], on="genus_con", how="left")
    df_comp = df_comp[~df_comp.filter(like="name_ru").apply(frozenset, axis=1).duplicated()].reset_index(drop=True)
    df_comp["cohabitation_type"].fillna("neutral", inplace=True)
    df_comp = df_comp[["name_ru", "name_ru_x", "cohabitation_type"]]
    df_comp["is_compatability"] = 1
    df_adjacency: pd.DataFrame = nx.to_pandas_edgelist(get_adjacency_graph(species_in_parks, target_parks=target_parks))
    df_comp = df_comp.rename(columns={"name_ru": "source", "name_ru_x": "target"}).merge(
        df_adjacency[["source", "target", "weight"]],
        on=["source", "target"],
        how="left",
    )
    if target_parks is not None:
        df_comp = df_comp[df_comp["source"].isin(df_adjacency["source"].unique())]
    df_comp = df_comp.fillna(0.1)
    df_comp.loc[df_comp["weight"] != 0.1, "cohabitation_type"] = "has_cases"
    combined_graph = nx.from_pandas_edgelist(
        df_comp,
        "source",
        "target",
        ["weight", "cohabitation_type"],
        create_using=nx.MultiGraph(),
        edge_key="is_compatability",
    )

    plant_dict = plants[["name_ru", "name_latin", "id", "is_invasive", "plant_type"]]
    plant_dict.index = plant_dict["name_ru"]
    plant_dict = plant_dict.transpose()
    plant_dict = plant_dict[plant_dict.index != "name_ru"].to_dict()
    nx.set_node_attributes(combined_graph, plant_dict)
    return combined_graph


def write_combined_graph_gexf(
    plants: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    species_in_parks: pd.DataFrame,
    target_parks: list[str] | None = None,
    output_path: str | BytesIO = "combined_graph.gexf",
) -> None:
    """
    Write combined graph with weights equal to number of co-occurence cases and compatability outcome in attributes
    to a given file (by name or a binary file-like object) in gexf format.
    """
    combined_graph = get_combined_graph(plants, cohabitation_attributes, species_in_parks, target_parks)
    nx.write_gexf(combined_graph, output_path)
