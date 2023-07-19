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
