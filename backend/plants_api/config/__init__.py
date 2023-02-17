# pylint: disable=too-many-instance-attributes
"""
Application configuration class is defined here.
"""
import os
from dataclasses import dataclass

from loguru import logger

from plants_api import __version__ as api_version


@dataclass
class AppSettings:
    """
    Configuration class for application.
    """

    host: str = "0.0.0.0"
    port: int = 8080

    db_addr: str = "localhost"
    db_port: int = 5432
    db_name: str = "plants_db"
    db_user: str = "postgres"
    db_pass: str = "postgres"
    debug: bool = False
    db_connect_retry: int = 20
    db_pool_size: int = 15
    photos_prefix: str = "localhost:6065/photo/"
    application_name = f"plants_api ({api_version})"

    @property
    def database_settings(self) -> dict[str, str | int]:
        """
        Get all settings for connection with database.
        """
        return {
            "host": self.db_addr,
            "port": self.db_port,
            "database": self.db_name,
            "user": self.db_user,
            "password": self.db_pass,
        }

    @property
    def database_uri(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}".format(**self.database_settings)

    @property
    def database_uri_sync(self) -> str:
        """
        Get uri for connection with database.
        """
        return "postgresql://{user}:{password}@{host}:{port}/{database}".format(**self.database_settings)

    @classmethod
    def try_from_env(cls) -> "AppSettings":
        """
        Call default class constructor, and then tries to find attributes
            values in environment variables by APP_{name}.
        """
        res = cls()
        for param, value in res.__dict__.items():
            if (env := f"APP_{param}") in os.environ or (env := param.upper()) in os.environ:
                logger.trace("Getting {} from envvar: {}", param, os.environ[env])
                setattr(res, param, type(value)(os.environ[env]))
        return res

    def update(self, other: "AppSettings") -> None:
        """
        Update current class attributes to the values of a given instance.
            Also set all values to environment with names APP_{name}.
        """
        for param, value in other.__dict__.items():
            if param in self.__dict__:
                os.environ[f"APP_{param}"] = str(value)
                setattr(self, param, value)


__all__ = [
    "AppSettings",
]
