"""
health_check endpoint is defined here.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection.session import get_connection
from plants_api.logic.compositions import get_global_territory
from plants_api.logic.plants import get_genera_cohabitation, get_plants_compositioner
from plants_api.schemas.basic_responses import OkResponse

from .routers import system_router


@system_router.post(
    "/system/refresh_caches",
    response_model=OkResponse,
    status_code=status.HTTP_200_OK,
)
async def refresh_caches(connection: AsyncConnection = Depends(get_connection)):
    """
    Refresh cached values for global territory, genera cohabitation and plants.
    """
    await get_global_territory(connection, use_cached=False)
    await get_plants_compositioner(connection, use_cached=False)
    await get_genera_cohabitation(connection, use_cached=False)

    return OkResponse()
