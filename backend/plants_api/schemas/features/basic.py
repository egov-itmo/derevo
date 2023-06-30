"""
Basic feature types which can be used for multiple entities are defined here.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class IdOnly:
    """
    Feature with only one attribute - id
    """

    id: int  # pylint: disable=invalid-name
