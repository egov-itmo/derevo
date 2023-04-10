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
from plants_api.logic.update import update_plants_from_xlsx
from plants_api.schemas.plants import PlantsResponse

from .routers import update_router


@update_router.post(
    "/xlsx",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
)
async def update_plants(
    connection: AsyncConnection = Depends(get_connection), file: UploadFile = File(...)
) -> PlantsResponse:
    """
    Get all plants information from the database.
    """
    logger.info("Updating plants from file {}", file.filename)
    content = BytesIO(await file.read())
    return (await update_plants_from_xlsx(connection, content)).getvalue()
