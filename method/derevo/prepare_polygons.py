"""
Polygons preparation logic is defined here.
"""
import itertools as it

import geopandas as gpd
import numpy as np
import pandas as pd
from loguru import logger


def make_grid(polygon, edge_size: int, polygon_id: int, crs: int = 32636) -> gpd.GeoDataFrame | None:
    """
    Return grid with given `edge_size`.
    """
    bounds = polygon.bounds
    x_coords = np.arange(bounds[0] + edge_size / 2, bounds[2], edge_size)
    y_coords = np.arange(bounds[1] + edge_size / 2, bounds[3], edge_size)
    combinations = np.array(list(it.product(x_coords, y_coords)))
    try:
        squaresult_lims = gpd.points_from_xy(combinations[:, 0], combinations[:, 1]).buffer(edge_size / 2, cap_style=3)
    except IndexError:
        logger.error("Index error at polygon_id={}", polygon_id)
        return None

    result_limsult = gpd.GeoDataFrame(
        gpd.GeoSeries(squaresult_lims[squaresult_lims.intersects(polygon)]),
        geometry=0,
        crs=crs,
    )
    result_limsult = gpd.GeoDataFrame(result_limsult.intersection(polygon), geometry=0, crs=crs).rename(
        columns={0: "geometry"}
    )
    result_limsult["id"] = polygon_id  # pylint: disable=unsupported-assignment-operation

    return result_limsult[["id", "geometry"]]  # pylint: disable=unsubscriptable-object


def get_ids(grid_id: pd.DataFrame) -> pd.DataFrame:
    """
    Unify identifiers in the given DataFrame.
    """
    ids = list(pd.unique(grid_id["lim_ids"]))
    new_lim_ids = []
    for i in ids:
        if isinstance(i, int):
            new_lim_ids.append(i)
        else:
            new_lim_ids.append([int(x) for x in i.split(",")])
    new_lim_ids = list(filter(lambda i: not isinstance(i, int), new_lim_ids))
    new_lim_ids = [v for l in new_lim_ids for v in l]
    grid_id = grid_id[~grid_id["lim_ids"].isin(new_lim_ids)]

    return grid_id


def green_lims(limitations: gpd.GeoDataFrame, greenery_polygons: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Overlay given limitations with greenery polygons.
    """
    lim_over = limitations.overlay(limitations, how="union").explode().dropna().reset_index(drop=True)
    lim_over["sorted"] = lim_over.apply(lambda x: "".join(sorted([str(x["id_1"]), str(x["id_2"])])), axis=1)
    lim_over = (
        lim_over.drop_duplicates(subset="sorted").drop("sorted", axis=1).sort_values("id_1").reset_index(drop=True)
    )

    whole = lim_over[(lim_over["id_1"]) == (lim_over["id_2"])]
    lim_over = lim_over[~lim_over.index.isin(whole.index)].reset_index(drop=True)
    lim_over["lim_ids"] = [
        int(x) if x == y else ",".join(sorted([str(int(x)), str(int(y))]))
        for x, y in list(zip(lim_over["limitation_factor_id_1"], lim_over["limitation_factor_id_2"]))
    ]
    lim_over = lim_over.drop(["limitation_factor_id_1", "limitation_factor_id_2"], axis=1)

    grid_parks = list(greenery_polygons.apply(lambda x: make_grid(x["geometry"], 5, x["id"]), axis=1))
    grid_parks = pd.concat(grid_parks).reset_index(drop=True)
    grid_parks = grid_parks.set_geometry("geometry")
    grid_parks["grid_id"] = range(len(grid_parks))

    parks_lims = grid_parks.sjoin(lim_over).reset_index(drop=True).drop(columns=["index_right"])
    grid_parks["lim_ids"] = np.nan
    parks_lims = parks_lims.drop_duplicates(["grid_id", "lim_ids"])

    parks_lims = parks_lims.groupby(["grid_id"]).apply(get_ids).reset_index(drop=True)
    result_lims = pd.merge(grid_parks, parks_lims[["grid_id", "lim_ids"]], on="grid_id", how="left")
    result_lims["lim_ids_x"] = result_lims["lim_ids_x"].fillna(result_lims["lim_ids_y"]).fillna(0)
    result_lims = result_lims.groupby(["id", "lim_ids_x"], as_index=False).apply(lambda x: x.unary_union)
    result_lims = result_lims.reset_index(drop=True).rename(columns={None: "geometry"})

    result_lims = gpd.GeoDataFrame(result_lims, geometry="geometry").set_crs(32636)

    return result_lims
