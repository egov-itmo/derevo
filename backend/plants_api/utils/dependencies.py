"""
FastApi dependencies are defined here.
"""
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncConnection
from plants_api.db.connection import get_connection
from plants_api.logic.users import get_user_info, validate_user_token
from plants_api.dto.users import User as UserDTO
from plants_api.exceptions.logic.users import AccessTokenExpiredError

from plants_api.utils.tokens import Token


def access_token_dependency(access_token: OAuth2PasswordBearer(tokenUrl="/api/login") = Depends()) -> Token:
    """
    Return token constructed from JWT token given in `Authorization` header.
    """
    return Token.from_jwt(access_token)


async def user_dependency(
    access_token: Token = Depends(access_token_dependency),
    conn: AsyncConnection = Depends(get_connection),
) -> UserDTO:
    """
    Return user fetched from the database by email from a validated access token.

    Ensures that User is active and valid.
    """
    if not await validate_user_token(conn, access_token):
        raise AccessTokenExpiredError(access_token)
    return await get_user_info(conn, access_token.email)
