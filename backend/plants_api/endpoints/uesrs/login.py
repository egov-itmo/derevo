# pylint: disable=too-many-arguments
"""
Login (authorization) endpoint is defined here.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncConnection
from starlette import status

from plants_api.db.connection import get_connection
from plants_api.logic.users import authorize
from plants_api.logic.users import refresh_tokens as refresh
from plants_api.schemas.users import LoginResponse
from plants_api.utils.tokens import Token

from .router import user_data_router


@user_data_router.post("/login", status_code=status.HTTP_200_OK)
async def authorize_user(
    device: str = "default",
    form_data: OAuth2PasswordRequestForm = Depends(),
    conn: AsyncConnection = Depends(get_connection),
) -> LoginResponse:
    """
    Authorizes user by given username (email or name) and password if user exists and active.

    Return access and refresh tokens, which user would need to store and send
    in `Authorization` header with requests later.

    If the given device value was already set for other token of a given user, then old token is overwrited.
    """
    tokens = await authorize(conn, device, form_data.username, form_data.password)
    return LoginResponse(access_token=tokens.access, refresh_token=tokens.refresh)


@user_data_router.post("/refresh_tokens", status_code=status.HTTP_200_OK)
async def refresh_tokens(
    refresh_token: str,
    conn: AsyncConnection = Depends(get_connection),
) -> LoginResponse:
    """
    Return access and refresh tokens for a given refresh token if it is valid and user is active.

    Returns access and refresh tokens, which user would need to store and send
    in `Authorization` header with requests later.

    If the given device value was already set for other token of a given user, then old token is overwrited.
    """
    token = Token.from_jwt(refresh_token)
    tokens = await refresh(conn, token)
    return LoginResponse(access_token=tokens.access, refresh_token=tokens.refresh)
