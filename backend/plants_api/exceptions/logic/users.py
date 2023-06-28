"""
User-related exceptions are defined here.
"""
from fastapi import status

from plants_api.exceptions import PlantsApiError


class UserExistsError(PlantsApiError):
    """
    Thrown on registration attempt when user with requested email already exists.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 400 Bad Request http code.
        """
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return f"User with given email ({self.email}) already exists"


class UserNotFoundError(PlantsApiError):
    """
    Thrown on login attempt when user with requested email does not exist.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return f"User with given email ({self.email}) does not exist"


class UserNotApprovedError(PlantsApiError):
    """
    Thrown on login attempt when user was not approved.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return f"User ({self.email}) was not approved to login"


class UserCredentialsInvalidError(PlantsApiError):
    """
    Thrown on login attempt when password hash did not match requested user password hash.
    """

    def __init__(self, email: str):
        self.email = email
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return f"User ({self.email}) login failed, password does not match"


class AccessTokenExpiredError(PlantsApiError):
    """
    Thrown on access request after token expiration time or if an access token was changed by refresh token.
    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Access token was provided, but it is invalid (expired or was refreshed already)"


class AccessWithdrawnError(PlantsApiError):
    """
    Thrown on access request with token from a device which access was withdrawn (is_active=False).
    """

    def __init__(self, access_token: str):
        self.access_token = access_token
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Access token was provided, but device was withdrawn"


class RefreshTokenNotFoundError(PlantsApiError):
    """
    Thrown on refresh request when no refresh token for a user with a given device is found.
    """

    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Refresh is not found, authorize again"


class RefreshTokenExpiredError(PlantsApiError):
    """
    Thrown on refresh request after token expiration time or if a refreh token was already refreshed.
    """

    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 401 Unauthorized response code.
        """
        return status.HTTP_401_UNAUTHORIZED

    def __str__(self) -> str:
        return "Refresh token is expired or was refreshed already"


class AccessTokenUsedToRefreshError(PlantsApiError):
    """
    Thrown on refresh request with an access token given.
    """

    def __init__(self, token: str):
        self.token = token
        super().__init__()

    def get_status_code(self) -> int:
        """
        Return 400 Bad Request http code.
        """
        return status.HTTP_400_BAD_REQUEST

    def __str__(self) -> str:
        return "Token refresh requested with access token given"
