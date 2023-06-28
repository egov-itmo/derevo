"""
Registration logic is defined here.
"""
from datetime import datetime, timezone

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection

from plants_api.db.entities.users import users, users_auth
from plants_api.dto.users import TokensTuple
from plants_api.exceptions.logic.users import (
    AccessTokenUsedToRefreshError,
    AccessWithdrawnError,
    RefreshTokenExpiredError,
    RefreshTokenNotFoundError,
    UserCredentialsInvalidError,
    UserNotApprovedError,
    UserNotFoundError,
)
from plants_api.utils.cryptography import hash_password
from plants_api.utils.tokens import Token, generate_tokens


async def authorize(conn: AsyncConnection, device: str, email: str, password: str) -> TokensTuple:
    """
    Returns an access and refresh tokens for a user if user with given login (email or name)"
        exists and password hash matched
    """
    statement = select(users.c.id, users.c.password_hash, users.c.is_approved).where(users.c.email == email)
    res = (await conn.execute(statement)).fetchone()
    if res is None:
        raise UserNotFoundError(email)
    user_id, password_hash, is_approved = res
    if not is_approved:
        raise UserNotApprovedError(email)
    if hash_password(email, password) != password_hash:
        raise UserCredentialsInvalidError(email)

    access_token, refresh_token = generate_tokens(email, device)
    statement = (
        insert(users_auth)
        .values(
            user_id=user_id,
            device=device,
            is_active=True,
            valid_until=access_token.exp,
            refresh_until=refresh_token.exp,
        )
        .on_conflict_do_update(
            "users_auth_unique_user_id_device",
            set_={"valid_until": access_token.exp, "refresh_until": refresh_token.exp, "is_active": True},
        )
    )
    await conn.execute(statement)
    await conn.commit()
    return TokensTuple(access_token.to_jwt(), refresh_token.to_jwt())


async def refresh_tokens(conn: AsyncConnection, refresh_token: Token) -> TokensTuple:
    """
    Returns an access and refresh tokens for a given refresh token if it is valid and user is active
    """
    if refresh_token.type != "refresh":
        raise AccessTokenUsedToRefreshError(refresh_token.to_jwt())
    if refresh_token.exp < datetime.now(timezone.utc):
        raise RefreshTokenExpiredError(refresh_token.to_jwt())
    statement = (
        select(users_auth.c.id, users.c.is_approved, users_auth.c.is_active, users_auth.c.refresh_until)
        .select_from(users_auth)
        .join(users, users_auth.c.user_id == users.c.id)
        .where((users.c.email == refresh_token.email) & (users_auth.c.device == refresh_token.device))
    )
    res = (await conn.execute(statement)).fetchone()
    if res is None:
        raise RefreshTokenNotFoundError(refresh_token.to_jwt())
    users_auth_id, user_is_approved, is_token_active, refresh_until = res
    if not user_is_approved:
        raise UserNotApprovedError(refresh_token.email)
    if not is_token_active:
        raise AccessWithdrawnError(refresh_token.to_jwt())
    if refresh_until != refresh_token.exp:
        raise RefreshTokenExpiredError(refresh_token.to_jwt())

    access_token, refresh_token = generate_tokens(refresh_token.email, refresh_token.device)
    statement = (
        update(users_auth)
        .values(
            is_active=True,
            valid_until=access_token.exp,
            refresh_until=refresh_token.exp,
        )
        .where(users_auth.c.id == users_auth_id)
    )
    await conn.execute(statement)
    await conn.commit()
    return TokensTuple(access_token.to_jwt(), refresh_token.to_jwt())
