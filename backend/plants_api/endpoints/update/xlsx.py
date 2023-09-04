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
from plants_api.schemas.basic_responses import OkResponse
from plants_api.schemas.update import SheetsConfiguration
from plants_api.utils.dependencies import user_dependency

from .router import update_router


_sheets_configuration = SheetsConfiguration()


@update_router.get(
    "/xlsx_sheet_configuration",
    response_model=SheetsConfiguration,
    status_code=status.HTTP_200_OK,
)
async def get_sheets_configuration() -> SheetsConfiguration:
    """Set sheets configuration of the xlsx file used for update"""
    return _sheets_configuration


@update_router.post(
    "/xlsx_sheet_configuration",
    response_model=OkResponse,
    status_code=status.HTTP_200_OK,
)
async def update_sheets_configuration(config: SheetsConfiguration) -> OkResponse:
    """Set sheets configuration of the xlsx file used for update"""
    global _sheets_configuration  # pylint: disable=global-statement
    _sheets_configuration = config
    return OkResponse()


@update_router.post(
    "/xlsx",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
)
async def update_plants(
    file: UploadFile = File(...),
    user: User = Depends(user_dependency),
    connection: AsyncConnection = Depends(get_connection),
) -> PlainTextResponse:
    """
    Get all plants information from the database.
    """
    logger.info("User {} requested plants update from file {}", user, file.filename)
    with BytesIO(await file.read()) as content:
        return (await update_plants_from_xlsx(connection, content, _sheets_configuration)).getvalue()
