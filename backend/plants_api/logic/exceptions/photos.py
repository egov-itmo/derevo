"""
Exceptions connected with geometry are defined here.
"""
from fastapi import status

from plants_api.utils.exceptions import PlantsApiError


class PhotoOpenError(PlantsApiError):
    """
    Exception to raise when the plant photo cannot be read with PIL.
    """

    def __init__(self, plant_id: int):
        """
        Construct from plant identifier for which photo has intended to be.
        """
        self.plant_id = plant_id
        super().__init__()

    def __str__(self) -> str:
        return f"The given photo cannot be read to set to the plant with id={self.plant_id}" + (
            f" (error was {self.__cause__})" if self.__cause__ is not None else ""
        )

    def get_status_code(self) -> int:
        """
        Return '400 Bad Request' status code.
        """
        return status.HTTP_400_BAD_REQUEST
