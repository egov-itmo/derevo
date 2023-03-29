"""
get_plants endpoint is defined here.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.logic.plants import get_plants_from_db
from plants_api.schemas.plants import PlantsResponse

from .routers import plants_router


@plants_router.get(
    "/all",
    response_model=PlantsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_plants(connection: AsyncConnection = Depends(get_connection)) -> PlantsResponse:
    """
    Get all plants information from the database.
    """
    plants = await get_plants_from_db(connection)
    return PlantsResponse.from_dtos(plants)
