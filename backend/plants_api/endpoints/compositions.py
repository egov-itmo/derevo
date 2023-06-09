"""
get_compositions endpoint is defined here.
"""
from typing import Any
from compositioner import Territory
from compositioner import enumerations as c_enum
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.logic.compositions import get_global_territory, get_plants_compositions, get_territory
from plants_api.logic.plants import get_genera_cohabitation, get_plants_by_ids, get_plants_from_db
from plants_api.schemas.compositions import CompositionsResponse
from plants_api.schemas.geojson import Geometry
from plants_api.schemas.plants import PlantsResponse
from plants_api.utils.adapters.plants import plant_dto_to_compositioner_plant

from .routers import compositions_router


@compositions_router.post(
    "/get_by_polygon",
    response_model=CompositionsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_compositions(  # pylint: disable=too-many-arguments
    territory: Geometry,
    plants_present: list[int] | None = None,
    light_type: c_enum.LightType | None = None,
    humidity_type: c_enum.HumidityType | None = None,
    soil_type: c_enum.SoilType | None = None,
    soil_fertility_type: c_enum.FertilityType | None = None,
    soil_acidity_type: c_enum.AcidityType | None = None,
    connection: AsyncConnection = Depends(get_connection),
) -> PlantsResponse:
    """
    Get all plants information from the database.
    """
    # TODO: cache following three values
    plants_available_cm = await plant_dto_to_compositioner_plant(connection, await get_plants_from_db(connection))
    global_territory = await get_global_territory(connection)
    genus_cohabitation = await get_genera_cohabitation(connection)

    plants_present_cm = await plant_dto_to_compositioner_plant(
        connection, await get_plants_by_ids(connection, plants_present) if plants_present is not None else []
    )
    territory_cm = get_territory(territory.as_shapely_geometry(), global_territory)

    def _listify(value: Any) -> list | None:
        return [value] if value is not None else None

    territory_cm.update(
        Territory(
            light_types=_listify(light_type),
            humidity_types=_listify(humidity_type),
            soil_types=_listify(soil_type),
            soil_acidity_types=_listify(soil_acidity_type),
            soil_fertility_types=_listify(soil_fertility_type),
        )
    )
    compositions = await get_plants_compositions(
        connection, plants_available_cm, territory_cm, genus_cohabitation, plants_present_cm
    )
    return CompositionsResponse.from_dtos(compositions)
