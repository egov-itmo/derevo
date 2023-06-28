"""
Registration logic is defined here.
"""
from loguru import logger
from sqlalchemy import exists, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities.users import users
from plants_api.exceptions.logic.users import UserExistsError
from plants_api.utils.cryptography import hash_password


async def register(conn: AsyncConnection, email: str, password: str) -> None:
    """
    Register a user if the given email, login and password if email and login are both available.
    """
    statement = exists(1).where(users.c.email == email).select()
    user_exists = (await conn.execute(statement)).scalar()
    if user_exists:
        raise UserExistsError(email)
    statement = insert(users).values(email=email, password_hash=hash_password(email, password))
    await conn.execute(statement)
    logger.info("Registered user {}", email)
    await conn.commit()
