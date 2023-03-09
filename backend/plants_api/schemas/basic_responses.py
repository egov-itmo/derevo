# pylint: disable=no-name-in-module, too-few-public-methods
"""
Basic responses are defined here.
"""
from typing import Literal

from pydantic import BaseModel


class OkResponse(BaseModel):
    """
    Response which is returned when request succseeded
    """

    result: Literal["Ok"] = "Ok"
