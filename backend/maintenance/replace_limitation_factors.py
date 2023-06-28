"""
Replace limitation factors layer with given name by
"""
from io import BytesIO
import json
import os
from pathlib import Path
import sys

import click

import requests

if "USE_PYGEOS" not in os.environ:
    os.environ["USE_PYGEOS"] = "0"
import geopandas as gpd  # pylint: disable=wrong-import-position


@click.command("replace_lf")
@click.option("--backend_address", "-b", default="http://localhost:8080", help="Backend host address")
@click.option(
    "--limitation_factor_type",
    "-t",
    help="Name (or id) of a limitation factor to replace layer",
    show_default="(asked on launch)",
)
@click.option(
    "--email",
    "-e",
    envvar="EMAIL",
    help="User email to login",
    prompt=True,
    show_default="(asked on lunch)",
    show_envvar=True,
)
@click.option(
    "--password",
    "-p",
    envvar="PASSWORD",
    help="User password to login",
    prompt=True,
    hide_input=True,
    show_default="(asked on lunch)",
    show_envvar=True,
)
@click.argument("new_limitation_factors", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def main(backend_address: str, limitation_factor_type: str, new_limitation_factors: Path, email: str, password: str):
    """
    Read given geojson file and use
    """
    try:
        version = requests.get(f"{backend_address}/api/openapi", timeout=10).json()["info"]["version"]
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error on connection to API backend at '{backend_address}/api/openapi': {exc!r}")
        sys.exit(1)
    print(f"Using API at '{backend_address}' - version {version}")

    gdf: gpd.GeoDataFrame = gpd.read_file(new_limitation_factors)
    if gdf.crs != 4326:
        gdf = gdf.to_crs(4326)

    limitation_factor_types: list[dict[str, int | str]] = requests.get(
        f"{backend_address}/api/listing/limitation_factors", timeout=10
    ).json()["values"]
    print(
        "Limitation factor ids: {}".format(  # pylint: disable=consider-using-f-string
            ", ".join(f"{lf['name']} -> {lf['id']}" for lf in limitation_factor_types)
        )
    )

    if limitation_factor_type is None:
        limitation_factor_type = input("Input limitation factor type to replace: ").strip()

    lft_id: int
    if limitation_factor_type.isnumeric():
        lft_id = int(limitation_factor_type)
        if lft_id not in (lft["id"] for lft in limitation_factor_types):
            print(f"limitation factor id '{limitation_factor_type}' is not in the limitation factors")
            sys.exit(1)
    else:
        if limitation_factor_type not in (lft["name"] for lft in limitation_factor_types):
            print(f"limitation factor name '{limitation_factor_type}' is not in the limitation factors")
            sys.exit(1)
        lft_id = next((lft["id"] for lft in limitation_factor_types if lft["name"] == limitation_factor_type))

    try:
        response = requests.post(
            f"{backend_address}/api/login?device=updater",
            data={"username": email, "password": password},
            timeout=60,
        )
        access_token = "Bearer " + response.json()["access_token"]
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Could not perform a login: {exc!r}")
        print(f"Response: {response.text}")
        sys.exit(1)
    headers = {"Authorization": access_token}

    response = requests.post(
        f"{backend_address}/api/update/limitation_factors/get_all/{lft_id}",
        timeout=60,
        headers=headers,
    )
    if response.status_code != 200:
        print(f"Limitation factor polygons request failed: {response.text[:1000]}")
        sys.exit(1)
    ids = [feature["properties"]["id"] for feature in response.json()["features"]]

    res = input(
        f"Replace {len(ids)} limitation factor polygons of id={lft_id} with {gdf.shape[0]} given polygons? [y/n] "
    )
    if res.lower() not in ("y", "1", "+"):
        print(f"Got '{res}' choice, exiting")
        sys.exit()

    try:
        response = requests.delete(
            f"{backend_address}/api/update/limitation_factors", json={"ids": ids}, headers=headers, timeout=60
        )
        if response.status_code != 200:
            print(f"Could not delete old limitation factors (status={response.status_code}): {response.text[:1000]}")
            sys.exit(1)

    except Exception as exc:  # pylint: disable=broad-except
        print(f"Could not delete old limitation factors: {exc!r}")
        sys.exit(1)

    buffer = BytesIO()
    gdf.to_file(buffer, driver="GeoJSON")  # GeoJSON in buffer to get geometries
    data = json.loads(buffer.getvalue())  # json data as dict
    try:
        response = requests.post(
            f"{backend_address}/api/update/limitation_factors",
            json={
                "limitation_factors": [
                    {"geometry": feature["geometry"], "limitation_factor_id": lft_id} for feature in data["features"]
                ]
            },
            headers=headers,
            timeout=60,
        )
        if response.status_code != 201:
            print(
                f"WARNING! Deleted old limitation factors, but could not insert new (status={response.status_code}): {response.text[:1000]}"
            )
            sys.exit(1)

    except Exception as exc:  # pylint: disable=broad-except
        print(f"WARNING! Deleted old limitation factors, but could not insert new: {exc!r}")


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
