"""
Limitation DTO is defined here.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Limitation:
    """
    Limitation model
    """

    id: int  # pylint: disable=invalid-name
    name: str
