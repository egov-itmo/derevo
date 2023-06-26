"""
Registration logic is defined here.
"""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities.users import users, users_auth
from plants_api.dto.users import User as UserDTO
from plants_api.exceptions.logic.users import UserNotFoundError
from plants_api.utils.tokens import Token


async def get_user_info(conn: AsyncConnection, email: str) -> UserDTO:
    """
    Return the information of given user by email.
    """
    statement = select(
        users.c.id,
        users.c.is_approved,
        users.c.registered_at,
    ).where((users.c.email == email))
    user = (await conn.execute(statement)).fetchone()
    if user is None:
        raise UserNotFoundError(email)
    return UserDTO(user[0], email, user[1], user[2])


async def validate_user_token(conn: AsyncConnection, token: Token) -> bool:
    """
    Check that token is not expired and active in the database. Return true if token is valid.
    """
    if token.exp < datetime.now(timezone.utc):
        return False

    statement = select(users_auth.c.valid_until).where(
        (users_auth.c.user_id == select(users.c.id).where(users.c.email == token.email).scalar_subquery())
        & (users_auth.c.device == token.device)
    )
    valid_until = (await conn.execute(statement)).fetchone()
    if valid_until is None:
        return False

    valid_until = valid_until[0]
    return valid_until == token.exp
