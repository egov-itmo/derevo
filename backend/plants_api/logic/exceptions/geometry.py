"""
Exceptions connected with geometry are defined here.
"""
from fastapi import status

from plants_api.utils.exceptions import PlantsApiError


class TooLargeGeometryError(PlantsApiError):
    """
    Exception to raise when the given geometry area is larger than maximum.
    """

    def __init__(self, area_max: float, area_given: float):
        """
        Column and table refer to the database entities, value is an already existing value given by user.
        """
        self.area_max = area_max
        self.area_given = area_given
        super().__init__()

    def __str__(self) -> str:
        return f"Area of a given geometry exceeds the maximum value of {self.area_max}: {self.area_given}"

    def get_status_code(self) -> int:
        """
        Return '400 Bad Request' status code.
        """
        return status.HTTP_400_BAD_REQUEST
