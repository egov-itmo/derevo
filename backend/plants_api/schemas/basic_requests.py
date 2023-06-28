# pylint: disable=no-name-in-module, too-few-public-methods
"""
Basic request schemas are defined here.
"""
from pydantic import BaseModel


class IdsRequest(BaseModel):
    """
    List of identifiers inserted.
    """

    ids: list[int]

    def to_list(self) -> list[int]:
        """
        Construct IdsResponse from list of identifiers.
        """
        return self.ids
