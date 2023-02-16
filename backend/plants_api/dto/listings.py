"""
Listing DTO is defined here.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ListingDto:
    """
    This DTO is used by listing endpoints logic.
    """

    id: int
    name: str
