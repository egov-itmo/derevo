# pylint: disable=no-name-in-module, too-few-public-methods
"""
Basic response schemas are defined here.
"""
from typing import Literal

from pydantic import BaseModel


class OkResponse(BaseModel):
    """
    Response which is returned when request succseeded
    """

    result: Literal["Ok"] = "Ok"


class IdsResponse(BaseModel):
    """
    List of identifiers inserted.
    """

    ids: list[int]

    @classmethod
    def from_list(cls, ids: list[int]) -> "IdsResponse":
        """
        Construct IdsResponse from list of identifiers.
        """
        return cls(ids=ids)
