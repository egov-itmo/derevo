# pylint: disable=redefined-builtin
"""
Token (JSON Web Token) class and functions to work with it are defined here.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt

from plants_api.config.app_settings_global import app_settings
from plants_api.exceptions.utils.exceptions import JWTDecodeError


class Token:
    """
    JWT Token class to operate on token payload data.
    """

    def __init__(self, type: Literal["access", "refresh"], email: str, device: str, exp: datetime = ..., **kwargs):
        """
        Token initialization from user email and devide. Expiration time can be set explicitly,
            but set by default according to token type anyway.
        """
        if isinstance(exp, Ellipsis.__class__):
            exp = datetime.now(timezone.utc).replace(microsecond=0) + timedelta(
                seconds=(
                    app_settings.jwt_access_token_exp_time
                    if type == "access"
                    else app_settings.jwt_refresh_token_exp_time
                )
            )
        self.data = {
            "type": type,
            "email": email,
            "device": device,
            "exp": exp,
            **kwargs,
        }

    def __repr__(self):
        return (
            f"JWT Token(type={self.data['type']}, email={self.data['email']},"
            f" device={self.data['device']}, exp={self.data['exp']}"
            + (")" if len(self.data) != 4 else f", and {len(self.data) - 4} more)")
        )

    def __str__(self):
        return f"Token({self.data['type']}, {self.data['email']}, device={self.data['device']}, exp={self.data['exp']})"

    def __getitem__(self, key: Any) -> Any:
        return self.data[key]

    @property
    def type(self) -> Literal["access", "refresh"]:
        """
        Token type ("access" or "refresh").
        """
        return self.data["type"]

    @property
    def email(self) -> str:
        """
        User email encoded in token.
        """
        return self.data["email"]

    @property
    def device(self) -> str:
        """
        User device encoded in token.
        """
        return self.data["device"]

    @property
    def exp(self) -> datetime:
        """
        Token expiration date and time.
        """
        return self.data["exp"]

    def __getattr__(self, name: str) -> Any:
        """
        Other attributes of token (if present).
        """
        return self.data[name]

    def to_jwt(self) -> str:
        """
        Encode token to JWT string format.
        """
        return jwt.encode(
            self.data,
            app_settings.jwt_secret_key,
            algorithm="HS256",
        )

    @classmethod
    def from_jwt(cls, jwt_str: str) -> "Token":
        """
        Construct Token class from jwt encoded to string.
        """
        try:
            data = jwt.decode(jwt_str, app_settings.jwt_secret_key, "HS256")
            assert isinstance(data, dict), "token value is not a dict"
            assert all(
                key in data for key in ("type", "email", "device", "exp")
            ), "token data is missing some essential keys"
            data["exp"] = datetime.fromtimestamp(data["exp"], timezone.utc)
        except Exception as exc:
            raise JWTDecodeError(jwt_str) from exc
        return cls(**data)


def generate_tokens(email: str, device: str) -> tuple[Token, Token]:
    """
    Generate access and refresh tokens for a given user.
    """
    return Token("access", email, device), Token("refresh", email, device)
