"""
update endpoint is defined here.
"""
from fastapi import Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.dto.users.user import User
from plants_api.logic.update import insert_limitation_factors
from plants_api.schemas.basic_responses import IdsResponse
from plants_api.schemas.update.limitation_factors import LimitationFactorsGeometryInsertionRequest
from plants_api.utils.dependencies import user_dependency

from .router import update_router


@update_router.post(
    "/limitation_factors",
    response_model=IdsResponse,
    status_code=status.HTTP_200_OK,
)
async def add_limitation_factors(
    limitation_factors: LimitationFactorsGeometryInsertionRequest,
    user: User = Depends(user_dependency),
    connection: AsyncConnection = Depends(get_connection),
) -> IdsResponse:
    """
    Insert given limitation factors to the database.
    """
    logger.info("Inserting {} limitation factors by user {}", len(limitation_factors.limitation_factors), user.email)
    return IdsResponse.from_list(await insert_limitation_factors(connection, limitation_factors.to_dto()))
