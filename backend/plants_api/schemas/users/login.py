"""
Login (authorization) response is defined here.

Login request is not needed due to use of OAuth2PasswordRequestForm from fastapi.security.
"""
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class LoginResponse(BaseModel):  # pylint: disable=too-few-public-methods
    """
    Response body class for login endpoint - contains access and refresh tokens.
    """

    access_token: str
    refresh_token: str
