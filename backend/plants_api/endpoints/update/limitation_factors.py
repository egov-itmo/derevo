"""
update endpoint is defined here.
"""
from typing import Any
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.dto.users import User
from plants_api.logic.limitations import get_all_limitation_factors
from plants_api.logic.update import delete_limitation_factors, insert_limitation_factors
from plants_api.schemas.basic_requests import IdsRequest
from plants_api.schemas.basic_responses import IdsResponse, OkResponse
from plants_api.schemas.features.basic import IdOnly
from plants_api.schemas.geojson import GeoJSONResponse
from plants_api.schemas.update.limitation_factors import LimitationFactorsGeometryInsertionRequest
from plants_api.utils.dependencies import user_dependency

from .router import update_router


@update_router.post(
    "/limitation_factors",
    response_model=IdsResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_limitation_factors(
    limitation_factors: LimitationFactorsGeometryInsertionRequest,
    user: User = Depends(user_dependency),
    connection: AsyncConnection = Depends(get_connection),
) -> IdsResponse:
    """
    Insert given limitation factor polygons to the database.
    """
    logger.info("Inserting {} limitation factors by user {}", len(limitation_factors.limitation_factors), user)
    return IdsResponse.from_list(await insert_limitation_factors(connection, limitation_factors.to_dto()))


@update_router.post(
    "/limitation_factors/get_all/{type_id}",
    response_model=GeoJSONResponse[IdOnly],
    status_code=status.HTTP_200_OK,
)
async def get_limitation_factors_by_type(
    type_id: int,
    _user: User = Depends(user_dependency),
    connection: AsyncConnection = Depends(get_connection),
) -> GeoJSONResponse[IdOnly]:
    """
    Get all limitation factor polygons of the given limitation factor from the database.
    """
    return await GeoJSONResponse[dict[str, Any]].from_list(await get_all_limitation_factors(connection, type_id))


@update_router.delete(
    "/limitation_factors",
    response_model=OkResponse,
    status_code=status.HTTP_200_OK,
)
async def remove_limitation_factors(
    limitation_factors_ids: IdsRequest,
    user: User = Depends(user_dependency),
    connection: AsyncConnection = Depends(get_connection),
) -> IdsResponse:
    """
    Delete limitation factor polygons with given ids from the database.
    """
    logger.info("Deleting {} limitation factors by user {}", len(limitation_factors_ids.ids), user)
    await delete_limitation_factors(connection, limitation_factors_ids.ids)
    return OkResponse()
