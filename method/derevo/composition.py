# pylint: disable=too-many-arguments,too-many-locals
"""
Composition-related methods are defined here.
"""
from __future__ import annotations

from io import BytesIO
from typing import Iterable

import geopandas as gpd
import networkx as nx
import pandas as pd
from loguru import logger
from networkx.algorithms.community import greedy_modularity_communities

from derevo.adjacency import get_adjacency_graph
from derevo.compatability import get_compatability_graph
from derevo.models import Plant, Territory
from derevo.models.cohabitation import GeneraCohabitation
from derevo.models.enumerations import ToleranceType


def get_compositions(
    plants_available: list[Plant],
    territory: Territory,
    cohabitation_attributes: list[GeneraCohabitation],
    plants_present: list[Plant] | None = None,  # FIXME plants_present are definetly not used now
) -> list[list[Plant]]:
    """
    Return plants composition variants list for the given parameters.
    """
    logger.debug(
        "Number of light conditions: {}, limitation factors: {}, humidity types: {}, soil types: {}, soil acidity types: {}, soil fertility types: {}, usda_zone: {}",
        len(territory.light_types) if territory.light_types is not None else "unknown",
        len(territory.limitation_factors) if territory.limitation_factors is not None else "unknown",
        len(territory.humidity_types) if territory.humidity_types is not None else "unknown",
        len(territory.soil_types) if territory.soil_types is not None else "unknown",
        len(territory.soil_acidity_types) if territory.soil_acidity_types is not None else "unknown",
        len(territory.soil_fertility_types) if territory.soil_fertility_types is not None else "unknown",
        territory.usda_zone.value if territory.usda_zone else "unknown",
    )
    if plants_present is None:
        logger.trace("None plants present")
        plants_present = []

    local_plants = pd.DataFrame(plants_available)

    if territory.light_types and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["light_preferences"].map(
                lambda x: len(x) == 0
                or any(x.get(lt, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE for lt in territory.light_types)
            )
        ]
    if territory.humidity_types and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["humidity_preferences"].map(
                lambda x: len(x) == 0
                or any(x.get(hd, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE for hd in territory.humidity_types)
            )
        ]
    if territory.soil_types and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["soil_type_preferences"].map(
                lambda x: len(x) == 0
                or any(x.get(st, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE for st in territory.soil_types)
            )
        ]
    if territory.soil_acidity_types and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["soil_acidity_preferences"].map(
                lambda x: len(x) == 0
                or any(
                    x.get(sa, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE for sa in territory.soil_acidity_types
                )
            )
        ]
    if territory.soil_fertility_types and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["soil_fertility_preferences"].map(
                lambda x: len(x) == 0
                or any(
                    x.get(sf, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE for sf in territory.soil_fertility_types
                )
            )
        ]
    if territory.limitation_factors and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["limitation_factors_resistances"].map(
                lambda x: len(x) == 0
                or all(
                    x.get(factor, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE
                    for factor in territory.limitation_factors
                )
            )
        ]
    if territory.usda_zone and local_plants.shape[0] != 0:
        local_plants = local_plants[
            local_plants["usda_zone_preferences"].map(
                lambda x: len(x) == 0 or x.get(territory.usda_zone, ToleranceType.NEUTRAL) != ToleranceType.NEGATIVE
            )
        ]
    if local_plants.shape[0] == 0:
        return [plants_present] if len(plants_present) != 0 else []

    cohabitation_df = pd.DataFrame(
        [(c.genus_1, c.genus_2, c.cohabitation.to_value()) for c in cohabitation_attributes],
        columns=["genus_name_1", "genus_name_2", "cohabitation_type"],
    )
    if local_plants.shape[0] > 1:
        compatability_graph: nx.Graph = get_compatability_graph(pd.DataFrame(plants_available), cohabitation_df)
        comp_graph = compatability_graph.subgraph(local_plants["name_ru"]).copy()
        communities_list = greedy_modularity_communities(comp_graph, weight="weight")
        logger.debug(
            "Number of communities: {} (sizes: {})",
            len(communities_list),
            ", ".join(map(str, (len(community) for community in communities_list))),
        )
        compositions = [list(com) for com in communities_list]
    else:
        compositions = [local_plants.iloc[0]["name_ru"]]

    present_names = {plant.name_ru for plant in plants_present}
    if (len(compositions) == 0 or all(len(composition) == 0 for composition in compositions)) and len(
        plants_present
    ) == 0:
        return []

    compositions = [
        plants_present
        + [plant for plant in plants_available if plant.name_ru in composition and plant.name_ru not in present_names]
        for composition in compositions
    ]
    return compositions


def _intersection_check(greenery_polygon: gpd.GeoDataFrame, factor: gpd.GeoDataFrame):
    """
    Determine if greenery polygon intersects with another polygon of light or limitation.
    """
    for i in factor.index:
        if greenery_polygon.intersects(factor.loc[i].geometry) is True:
            return True
    return False


def get_updated_composition(
    plants: pd.DataFrame,
    plants_with_limitations_resistance: pd.DataFrame,
    plants_suitable_for_light: pd.DataFrame,
    cohabitation_attributes: pd.DataFrame,
    limitations: gpd.GeoDataFrame,
    light: gpd.GeoDataFrame,
    species_in_parks: pd.DataFrame,
    greenery_polygon: gpd.GeoDataFrame,
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
    logger.debug("Number of communities: {}", len(communities_list))

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
    greenery_polygon: gpd.GeoDataFrame,
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
    greenery_polygon: gpd.GeoDataFrame,
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
    logger.debug("Number of communities: {}", len(communities_list))

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
    greenery_polygon: gpd.GeoDataFrame,
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
    logger.debug("Number of communities: {}", len(communities_list))
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
