# pylint: disable=too-many-arguments
"""
Registration endpoint is defined here.
"""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.logic.users import register
from plants_api.schemas.basic_responses import OkResponse
from plants_api.schemas.users import RegistrationRequest

from .router import user_data_router


@user_data_router.post("/register", status_code=status.HTTP_200_OK)
async def register_user(
    registration_request: RegistrationRequest,
    conn: AsyncConnection = Depends(get_connection),
) -> OkResponse:
    """
    Registers user by given email, name and password if they are all valid and no user with such email or name exist.
    """
    await register(conn, registration_request.email, registration_request.password)
    return OkResponse()
