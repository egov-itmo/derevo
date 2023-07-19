# pylint: disable=too-many-locals,too-many-statements,too-many-nested-blocks
"""
Get optimal resolution method is defined here.
"""
from __future__ import annotations

import itertools as it

import networkx as nx
import numpy as np
import pandas as pd
from loguru import logger
from matplotlib.axes import Axes
from networkx.algorithms.community import greedy_modularity_communities

from derevo.compatability import get_compatability_graph


def get_best_resolution(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    graph_axes: Axes | None = None,
) -> pd.DataFrame:
    """
    Return dataframe with calculated best resolutions for current collection of species
    and limitation factors / light variants.

    If `graph_axes` is given, scatter plot will be drawn on it.
    """
    plants = plants.copy()
    plants_with_lim_resist = plants_with_limitations_resistance.copy()
    plants_with_lig_resist = plants_suitable_for_light.copy()
    compatability_graph = get_compatability_graph(plants, cohabitation_attributes)
    lig_list = [1, 2, 3]
    lim_list = [1, 2, 3, 4, 5, 6]

    res_list = [x / 10 for x in range(0, 21, 1)]
    result: list[list] = []
    for lig in range(len(lig_list) + 1):
        for lig_subset in it.combinations(lig_list, lig):
            if len(list(lig_subset)) == 0:
                continue
            filtered_plants = plants_with_lig_resist[plants_with_lig_resist.light_type_id.isin(list(lig_subset))]
            light_comp = list(pd.unique(filtered_plants["name_ru"]))
            for lim in range(len(lim_list) + 1):
                for lim_subset in it.combinations(lim_list, lim):
                    filtered_plants = plants_with_lim_resist[
                        plants_with_lim_resist.limitation_factor_id.isin(list(lim_subset))
                    ]
                    limitations_comp = filtered_plants.groupby("name_ru").count().reset_index()
                    limitations_comp = limitations_comp[
                        limitations_comp.limitation_factor_id == limitations_comp.limitation_factor_id.max()
                    ]
                    limitations_comp = list(pd.unique(limitations_comp["name_ru"]))

                    # filtering species by environmental factors
                    df_comp = plants[plants["name_ru"].isin(light_comp)]
                    if len(lim_subset) > 0:
                        df_comp = df_comp[df_comp["name_ru"].isin(limitations_comp)]

                    comp_graph = compatability_graph.copy()
                    comp_graph = comp_graph.subgraph(df_comp["name_ru"])
                    default_size_of_community = comp_graph.number_of_nodes()
                    default_number_of_negative_edges = len(nx.to_pandas_edgelist(comp_graph).query("weight == 1"))
                    for res in res_list:
                        communities_list = greedy_modularity_communities(comp_graph, weight="weight", resolution=res)
                        size_of_biggest_community = max(len(com) for com in communities_list)
                        composition = [list(com) for com in communities_list if len(com) == size_of_biggest_community]
                        if len(composition) == default_size_of_community:
                            c_graph = comp_graph.subgraph(list(it.chain.from_iterable(composition)))
                            number_of_remaining_nodes = c_graph.number_of_nodes()
                            number_of_negative_edges = len(nx.to_pandas_edgelist(c_graph).query("weight == 1"))
                            tag = "One node community"
                            result.append(
                                [
                                    ", ".join(map(str, list(lig_subset)))
                                    + "; "
                                    + ", ".join(map(str, list(lim_subset))),
                                    list(pd.unique(df_comp["name_ru"])),
                                    communities_list,
                                    number_of_remaining_nodes,
                                    number_of_negative_edges,
                                    res,
                                    default_size_of_community,
                                    default_number_of_negative_edges,
                                    tag,
                                ]
                            )
                        elif len(composition) > 1:
                            for comp in composition:
                                c_graph = comp_graph.subgraph(comp)
                                number_of_remaining_nodes = c_graph.number_of_nodes()
                                number_of_negative_edges = len(nx.to_pandas_edgelist(c_graph).query("weight == 1"))
                                tag = "Variable community"
                                result.append(
                                    [
                                        ", ".join(map(str, list(lig_subset)))
                                        + "; "
                                        + ", ".join(map(str, list(lim_subset))),
                                        list(pd.unique(df_comp["name_ru"])),
                                        communities_list,
                                        number_of_remaining_nodes,
                                        number_of_negative_edges,
                                        res,
                                        default_size_of_community,
                                        default_number_of_negative_edges,
                                        tag,
                                    ]
                                )
                        else:
                            c_graph = comp_graph.subgraph(list(it.chain.from_iterable(composition)))
                            number_of_remaining_nodes = c_graph.number_of_nodes()
                            number_of_negative_edges = len(nx.to_pandas_edgelist(c_graph).query("weight == 1"))
                            tag = "Default community"
                            result.append(
                                [
                                    ", ".join(map(str, list(lig_subset)))
                                    + "; "
                                    + ", ".join(map(str, list(lim_subset))),
                                    list(pd.unique(df_comp["name_ru"])),
                                    communities_list,
                                    number_of_remaining_nodes,
                                    number_of_negative_edges,
                                    res,
                                    default_size_of_community,
                                    default_number_of_negative_edges,
                                    tag,
                                ]
                            )
                    logger.debug("lim_subset done: {}", list(lim_subset))
            logger.debug("lig_subset done: {}", list(lig_subset))
    df_result = pd.DataFrame(
        result,
        columns=[
            "variant_id",
            "precomposition",
            "communities_list",
            "size",
            "negative_edges",
            "resolution",
            "total_size",
            "total_edge_number",
            "tag",
        ],
    )
    df_result["share_of_nodes"] = df_result["size"] / df_result["total_size"]
    df_result["share_of_negative_edges"] = df_result["negative_edges"] / df_result["total_edge_number"]
    df_result["composition_improvement"] = df_result["share_of_nodes"] - df_result["share_of_negative_edges"]
    df_result["communities"] = df_result.communities_list.map(
        lambda x: [list(com) for com in x if len(com) == max(len(com) for com in x)]
    )
    df_result["communities"] = df_result.communities.map(lambda x: list(it.chain.from_iterable(x)))
    df_result["size"] = df_result.communities.map(len)

    if graph_axes is not None:
        x_axis = list(df_result["resolution"])
        y_axis = list(df_result["composition_improvement"])

        graph_axes.scatter(x_axis, y_axis, marker=0)
        graph_axes.set_xticks(np.arange(min(x_axis), max(x_axis), 0.1), rotation=90)
        graph_axes.set_yticks(np.arange(min(y_axis), max(y_axis), 0.1))
        graph_axes.grid(True)
        graph_axes.set_xlabel("resolution")
        graph_axes.set_ylabel("composition improvement")

    return df_result
