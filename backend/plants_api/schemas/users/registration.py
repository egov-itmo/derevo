"""
Registration request is defined here.
"""
from re import compile as re_compile
from re import match

from pydantic import BaseModel, validator  # pylint: disable=no-name-in-module


_email_re = re_compile(r"^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$")
_password_re = re_compile(r"^[\w!@#\$%\^&\*\(\)]+$")


class RegistrationRequest(BaseModel):  # pylint: disable=redefined-builtin,no-self-argument
    """
    Request body class given as a request for user registration endpoint.
    """

    email: str
    password: str

    @validator("email")
    def validate_email(email: str):  # pylint: disable=no-self-argument
        """
        Validate email with regular expression.
        """
        if match(_email_re, email) is None:
            raise ValueError(f"provided email address '{email}' is invalid")
        return email

    @validator("password")
    def validate_password(password: str):  # pylint: disable=no-self-argument
        """
        validate password with regular expression.
        """
        if match(_password_re, password) is None:
            raise ValueError(f"provided password '{password}' is invalid")
        return password
