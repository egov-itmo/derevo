"""
update endpoint is defined here.
"""
from io import BytesIO

from fastapi import Depends, File, UploadFile
from fastapi.responses import PlainTextResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.dto.users import User
from plants_api.logic.update import update_plants_from_xlsx
from plants_api.schemas.plants import PlantsResponse
from plants_api.utils.dependencies import user_dependency

from .router import update_router


@update_router.post(
    "/xlsx",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
)
async def update_plants(
    file: UploadFile = File(...),
    user: User = Depends(user_dependency),
    connection: AsyncConnection = Depends(get_connection),
) -> PlantsResponse:
    """
    Get all plants information from the database.
    """
    logger.info("User {} requested plants update from file {}", user, file.filename)
    content = BytesIO(await file.read())
    return (await update_plants_from_xlsx(connection, content)).getvalue()
