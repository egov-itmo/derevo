"""
get_compositions endpoint is defined here.
"""
from io import BytesIO
from typing import Any

from borb.pdf import PDF
from compositioner import Territory
from fastapi import Depends, Response
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.dto.plants import PlantDto
from plants_api.logic.compositions import get_global_territory, get_plants_compositions, get_territory
from plants_api.logic.pdf import compositions_to_pdf
from plants_api.logic.plants import get_genera_cohabitation, get_plants_by_ids, get_plants_compositioner
from plants_api.schemas.compositions import CompositionsResponse
from plants_api.schemas.geojson import Geometry
from plants_api.schemas.plants import PlantsResponse
from plants_api.utils.adapters.compositioner_enums import (
    get_humidity_type_by_id,
    get_light_type_by_id,
    get_soil_acidity_type_by_id,
    get_soil_fertility_type_by_id,
    get_soil_type_by_id,
)
from plants_api.utils.adapters.plants import plant_dto_to_compositioner_plant

from .routers import compositions_router


def _listify(value: Any) -> list | None:
    """
    Return list containing the only `value` element or `value` itself if it is a list.
    """
    if isinstance(value, list):
        return value
    return [value] if value is not None else []


async def _get_territory_information(  # pylint: disable=too-many-arguments
    connection: AsyncConnection,
    territory: Geometry,
    light_type_id: int | None = None,
    humidity_type_id: int | None = None,
    soil_type_id: int | None = None,
    soil_fertility_type_id: int | None = None,
    soil_acidity_type_id: int | None = None,
):
    """
    Get territory information from the database combined with given data.
    """
    global_territory = await get_global_territory(connection)

    light_type = await get_light_type_by_id(connection, light_type_id)
    humidity_type = await get_humidity_type_by_id(connection, humidity_type_id)
    soil_type = await get_soil_type_by_id(connection, soil_type_id)
    soil_fertility_type = await get_soil_fertility_type_by_id(connection, soil_fertility_type_id)
    soil_acidity_type = await get_soil_acidity_type_by_id(connection, soil_acidity_type_id)

    territory_cm = get_territory(territory.as_shapely_geometry(), global_territory)

    territory_cm.update(
        Territory(
            light_types=_listify(light_type),
            humidity_types=_listify(humidity_type),
            soil_types=_listify(soil_type),
            soil_acidity_types=_listify(soil_acidity_type),
            soil_fertility_types=_listify(soil_fertility_type),
        )
    )
    return territory_cm


async def _get_compositions(
    connection: AsyncConnection,
    territory_cm: Territory,
    plants_present: list[int] | None = None,
) -> list[list[PlantDto]]:
    plants_available_cm = await get_plants_compositioner(connection)
    genus_cohabitation = await get_genera_cohabitation(connection)

    if plants_present is not None:
        plants_present_cm = await plant_dto_to_compositioner_plant(
            connection,
            await get_plants_by_ids(connection, plants_present),
        )
    else:
        plants_present_cm = []

    return await get_plants_compositions(
        connection,
        plants_available_cm,
        territory_cm,
        genus_cohabitation,
        plants_present_cm,
    )


@compositions_router.post(
    "/get_by_polygon",
    response_model=CompositionsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_compositions(  # pylint: disable=too-many-arguments
    territory: Geometry,
    plants_present: list[int] | None = None,
    light_type_id: int | None = None,
    humidity_type_id: int | None = None,
    soil_type_id: int | None = None,
    soil_fertility_type_id: int | None = None,
    soil_acidity_type_id: int | None = None,
    connection: AsyncConnection = Depends(get_connection),
) -> PlantsResponse:
    """
    Get all plants information from the database.
    """
    territory_cm = await _get_territory_information(
        connection,
        territory,
        light_type_id,
        humidity_type_id,
        soil_type_id,
        soil_fertility_type_id,
        soil_acidity_type_id,
    )
    compositions = await _get_compositions(connection, territory_cm, plants_present)
    return CompositionsResponse.from_dtos(compositions)


@compositions_router.post(
    "/get_by_polygon/pdf",
    status_code=status.HTTP_200_OK,
)
async def get_compositions_pdf(  # pylint: disable=too-many-arguments
    territory: Geometry,
    plants_present: list[int] | None = None,
    light_type_id: int | None = None,
    humidity_type_id: int | None = None,
    soil_type_id: int | None = None,
    soil_fertility_type_id: int | None = None,
    soil_acidity_type_id: int | None = None,
    connection: AsyncConnection = Depends(get_connection),
) -> Response:
    """
    Get plants compositions as a PDF file.
    """
    territory_cm = await _get_territory_information(
        connection,
        territory,
        light_type_id,
        humidity_type_id,
        soil_type_id,
        soil_fertility_type_id,
        soil_acidity_type_id,
    )
    compositions = await _get_compositions(connection, territory_cm, plants_present)
    pdf = compositions_to_pdf(compositions, territory_cm)
    with BytesIO() as buffer:
        PDF.dumps(buffer, pdf)
        return Response(buffer.getvalue(), headers={"Content-Disposition": 'attachment; filename="compositions.pdf"'})
