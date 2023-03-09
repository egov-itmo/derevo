# pylint: disable=method-hidden, no-self-use
"""
Top exceptions for a plants backend service are defined here.
"""

from fastapi import status, HTTPException


class PlantsApiError(HTTPException):
    """
    Base Plants API exception to inherit from.
    User can redefine `status_code` method and `__str__` as its value will be used in HTTPException.
    """

    def __init__(self):
        super().__init__(self.status_code(), str(self))

    def status_code(self) -> int:
        """
        Return FastApi response status for an HTTPException. Descestors should override this method,
            but it defaults to 500 - Internal Server Error.
        """
        return status.HTTP_500_INTERNAL_SERVER_ERROR


class JWTDecodeError(PlantsApiError):
    """
    Thrown a failed attempt to decode JWT token value, either because a bad format or missing essential keys.
    """

    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def status_code(self) -> int:
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "JWT decoding decoding error"
