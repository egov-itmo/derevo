# pylint: disable=too-many-arguments,too-many-locals
"""
Composition-related methods are defined here.
"""
from io import BytesIO
from typing import Iterable

import geopandas as gpd
import networkx as nx
import pandas as pd
from loguru import logger
from networkx.algorithms.community import greedy_modularity_communities

from compositioner.get_adjacency import get_adjacency_graph
from compositioner.get_compatability import get_compatability_graph


def _intersection_check(greenery_polygon, factor: gpd.GeoDataFrame):
    """
    Determine if greenery polygon intersects with another polygon of light or limitation.
    """
    for i in factor.index:
        if greenery_polygon.intersects(factor.loc[i].geometry) is True:
            return True
    return False


def get_species_composition_old(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    limitations: gpd.GeoDataFrame,
    light: gpd.GeoDataFrame,
    greenery_polygon,
) -> str | None:  # TODO: need refactor
    """
    Return Series of strings with composition of plants.
    """
    plants = plants.copy()
    plants_with_lim_resist = plants_with_limitations_resistance.copy()
    plants_with_lig_resist = plants_suitable_for_light.copy()
    cohabitation = cohabitation_attributes.copy()
    limitations = limitations.copy()
    light = light.copy()

    # finding species which can grow in existing light conditions
    light_types = list(light["light_type_id"].unique())
    lig_list = [
        lig_id
        for lig_id in light_types
        if _intersection_check(greenery_polygon, light.query(f"light_type_id == {lig_id}"))
    ]
    filtered_plants = plants_with_lig_resist[plants_with_lig_resist["light_type_id"].isin(lig_list)]
    light_comp = list(filtered_plants["name_ru"].unique())
    logger.debug("number of light conditions: {}", len(lig_list))

    # finding species which can grow with existing limitations
    limitation_factors = list(limitations["limitation_factor_id"].unique())
    lim_list = [
        lim_id
        for lim_id in limitation_factors
        if _intersection_check(greenery_polygon, limitations.query(f"limitation_factor_id == {lim_id}"))
    ]
    filtered_plants = plants_with_lim_resist[plants_with_lim_resist["limitation_factor_id"].isin(lim_list)]
    limitations_comp: pd.DataFrame = filtered_plants.groupby("name_ru").count().reset_index()
    limitations_comp = limitations_comp[
        limitations_comp["limitation_factor_id"] == limitations_comp["limitation_factor_id"].max()
    ]
    limitations_comp = list(limitations_comp["name_ru"].unique())
    logger.debug("number of limitation factors: {}", len(lim_list))

    # filtering species by environmental factors
    if len(lig_list) > 0:
        df_comp = plants[plants["name_ru"].isin(light_comp)]
    else:
        logger.warning("no light conditions provided")
        return None
    if len(lim_list) > 0:
        df_comp = df_comp[df_comp["name_ru"].isin(limitations_comp)]

    # connecting with cohabitation weights
    edge_1 = df_comp.merge(cohabitation, left_on="genus_id", right_on="genus_id_1", how="left")
    edge_1.dropna(subset="genus_id_1", inplace=True)
    edge_2 = edge_1.merge(df_comp, left_on="genus_id_2", right_on="genus_id", how="left").rename(
        columns={
            "name_ru_x": "u",
            "name_ru_y": "v",
        }
    )[["u", "v", "cohabitation_type"]]
    edge_2.dropna(inplace=True)
    edge_2 = edge_2.rename(columns={"cohabitation_type": "weight"})
    edge_2["weight"].replace({"negative": 1, "neutral": 2, "positive": 3}, inplace=True)

    # creating graph and finding biggest community
    green_graph = nx.from_pandas_edgelist(edge_2, "u", "v", "weight")
    communities_list = greedy_modularity_communities(green_graph, weight="weight")
    size_of_biggest_community = max(len(com) for com in communities_list)

    logger.debug("biggest community has {} members", size_of_biggest_community)
    composition = ", ".join([", ".join(com) for com in communities_list if len(com) == size_of_biggest_community])

    return composition


def get_updated_composition(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    limitations: gpd.GeoDataFrame,
    light: gpd.GeoDataFrame,
    species_in_parks: pd.DataFrame,
    greenery_polygon,
) -> list[nx.Graph] | None:
    """
    Return list of graphs with variants of updated plants composition.
    """
    # version with all edges
    plants = plants.copy()
    plants_with_lim_resist = plants_with_limitations_resistance.copy()
    plants_with_lig_resist = plants_suitable_for_light.copy()
    limitations = limitations.copy()
    light = light.copy()

    # finding species which can grow in existing light conditions
    light_types = list(light["light_type_id"].unique())
    lig_list = [
        lig_id
        for lig_id in light_types
        if _intersection_check(greenery_polygon.geometry, light.query(f"light_type_id == {lig_id}"))
    ]
    filtered_plants = plants_with_lig_resist[plants_with_lig_resist["light_type_id"].isin(lig_list)]
    light_comp = list(filtered_plants["name_ru"].unique())
    logger.debug("number of light conditions: {}", len(lig_list))

    # finding species which can grow with existing limitations
    limitation_factors = list(limitations["limitation_factor_id"].unique())
    lim_list = [
        lim_id
        for lim_id in limitation_factors
        if _intersection_check(
            greenery_polygon.geometry,
            limitations.query(f"limitation_factor_id == {lim_id}"),
        )
    ]
    filtered_plants = plants_with_lim_resist[plants_with_lim_resist["limitation_factor_id"].isin(lim_list)]
    limitations_comp: pd.DataFrame = filtered_plants.groupby("name_ru").count().reset_index()
    limitations_comp = limitations_comp[
        limitations_comp["limitation_factor_id"] == limitations_comp["limitation_factor_id"].max()
    ]
    limitations_comp = list(limitations_comp["name_ru"].unique())
    logger.debug("number of limitation factors: {}", len(lim_list))

    # filtering species by environmental factors
    if len(lig_list) > 0:
        df_comp = plants[plants["name_ru"].isin(light_comp)]
    else:
        logger.warning("no light conditions provided")
        return None

    if len(lim_list) > 0:
        df_comp = df_comp[df_comp["name_ru"].isin(limitations_comp)]

    compatability_graph: nx.Graph = get_compatability_graph(plants, cohabitation_attributes)
    comp_graph = compatability_graph.copy()
    comp_graph = comp_graph.subgraph(df_comp["name_ru"])
    communities_list = greedy_modularity_communities(comp_graph, weight="weight")
    logger.debug("number of communities: {}", len(communities_list))

    compositions = [list(com) for com in communities_list]
    current_graph = get_adjacency_graph(species_in_parks, target_parks=[greenery_polygon["name"]])
    current_composition = list(nx.to_pandas_edgelist(current_graph).source.unique())

    graph_variants = []
    for composition in compositions:
        upd_comp = composition + current_composition
        updated_graph: nx.Graph = compatability_graph.subgraph(upd_comp)
        for node_id in composition:
            updated_graph.nodes[node_id]["is_added"] = True
        for node_id in current_composition:
            updated_graph.nodes[node_id]["is_added"] = False
        graph_variants.append(updated_graph)

    return graph_variants


def write_updated_composition_gexf(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    limitations: gpd.GeoDataFrame,
    light: gpd.GeoDataFrame,
    species_in_parks: pd.DataFrame,
    greenery_polygon,
    output_path_prefix: str | Iterable[BytesIO] | Iterable[str],
):
    """
    Write variants of updated plants composition to files with given prefix
    or names / file-like objects given in iterator.
    """
    graph_variants = get_updated_composition(
        plants,
        plants_with_limitations_resistance,
        plants_suitable_for_light,
        cohabitation_attributes,
        limitations,
        light,
        species_in_parks,
        greenery_polygon,
    )
    if graph_variants is None:
        logger.error("updated composition graph is not exported")
        return
    if isinstance(output_path_prefix, str):
        for graph in graph_variants:
            nx.write_gexf(graph, f"{output_path_prefix}_v_{graph_variants.index(graph)}.gexf")
    else:
        for graph, output in zip(graph_variants, output_path_prefix):
            nx.write_gexf(graph, output)


def get_recommended_composition(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    limitations: pd.DataFrame,
    light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    greenery_polygon,
) -> list[nx.Graph] | None:
    """
    Return list of graphs with variants of recommended composition with account for outer factors.
    """
    plants = plants.copy()
    plants_with_lim_resist = plants_with_limitations_resistance.copy()
    plants_with_lig_resist = plants_suitable_for_light.copy()
    limitations = limitations.copy()
    light = light.copy()

    # finding species which can grow in existing light conditions
    light_types = list(light["light_type_id"].unique())
    lig_list = [
        lig_id
        for lig_id in light_types
        if _intersection_check(greenery_polygon.geometry, light.query(f"light_type_id == {lig_id}"))
    ]
    filtered_plants = plants_with_lig_resist[plants_with_lig_resist["light_type_id"].isin(lig_list)]
    light_comp = list(filtered_plants["name_ru"].unique())
    logger.debug("number of light conditions: {}", len(lig_list))
    # finding species which can grow with existing limitations
    limitation_factors = list(limitations["limitation_factor_id"].unique())
    lim_list = [
        lim_id
        for lim_id in limitation_factors
        if _intersection_check(
            greenery_polygon.geometry,
            limitations.query(f"limitation_factor_id == {lim_id}"),
        )
    ]
    filtered_plants = plants_with_lim_resist[plants_with_lim_resist["limitation_factor_id"].isin(lim_list)]
    limitations_comp = filtered_plants.groupby("name_ru").count().reset_index()
    limitations_comp = limitations_comp[
        limitations_comp["limitation_factor_id"] == limitations_comp["limitation_factor_id"].max()
    ]
    limitations_comp = list(limitations_comp["name_ru"].unique())
    logger.debug("number of limitation factors: {}", len(lim_list))

    # filtering species by environmental factors
    if len(lig_list) > 0:
        df_comp = plants[plants["name_ru"].isin(light_comp)]
    else:
        logger.warning("no light conditions provided")
        return None
    if len(lim_list) > 0:
        df_comp = df_comp[df_comp["name_ru"].isin(limitations_comp)]

    compatability_graph = get_compatability_graph(plants, cohabitation_attributes)
    comp_graph = compatability_graph.copy()
    comp_graph = comp_graph.subgraph(df_comp["name_ru"])
    communities_list = greedy_modularity_communities(comp_graph, weight="weight")
    logger.debug("number of communities: {}", len(communities_list))

    compositions = [list(com) for com in communities_list]
    graph_variants = []
    for composition in compositions:
        recommended_graph = compatability_graph.subgraph(composition)
        for node_id in composition:
            recommended_graph.nodes[node_id]["is_added"] = True
        graph_variants.append(recommended_graph)

    return graph_variants


def write_recommended_composition_gexf(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    limitations: pd.DataFrame,
    light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    greenery_polygon,
    output_path_prefix: str | Iterable[BytesIO] | Iterable[str] = "recommended",
) -> None:
    """
    Write list of graphs with variants of recommended composition with account for outer factors
    to files with given prefix or names / file-like objects given in iterator.
    """
    graph_variants = get_recommended_composition(
        plants,
        plants_with_limitations_resistance,
        plants_suitable_for_light,
        limitations,
        light,
        cohabitation_attributes,
        greenery_polygon,
    )
    if graph_variants is None:
        logger.error("recommended composition graph is not exported")
        return
    if isinstance(output_path_prefix, str):
        for graph in graph_variants:
            nx.write_gexf(graph, f"{output_path_prefix}_v_{graph_variants.index(graph)}.gexf")
    else:
        for graph, output in zip(graph_variants, output_path_prefix):
            nx.write_gexf(graph, output)


def get_composition_unknown(
    plants: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
) -> list[nx.Graph]:
    """
    Return list of graphs with variants of recommended composition for a place with unknown outer factors.
    """
    compatability_graph = get_compatability_graph(plants, cohabitation_attributes)
    communities_list = greedy_modularity_communities(compatability_graph, weight="weight")
    logger.debug("number of communities: {}", len(communities_list))
    compositions = [list(com) for com in communities_list]
    graph_variants = []
    for composition in compositions:
        recommended_graph = compatability_graph.subgraph(composition)
        for node_id in composition:
            recommended_graph.nodes[node_id]["is_added"] = True
        recommended_graph.nodes.data("is_added", default=False)
        graph_variants.append(recommended_graph)
    return graph_variants


def write_composition_unknown_gfsx(
    plants: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    output_path_prefix: str | Iterable[BytesIO] | Iterable[str] = "new_graph",
) -> list[nx.Graph]:
    """
    Write graphs with variants of recommended composition for a place with unknown outer factors
    to files with given prefix or names / file-like objects given in iterator.
    """
    graph_variants = get_composition_unknown(plants, cohabitation_attributes)
    if isinstance(output_path_prefix, str):
        for graph in graph_variants:
            nx.write_gexf(graph, f"{output_path_prefix}_v_{graph_variants.index(graph)}.gexf")
    else:
        for graph, output in zip(graph_variants, output_path_prefix):
            nx.write_gexf(graph, output)
