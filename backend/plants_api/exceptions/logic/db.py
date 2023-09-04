"""
Exceptions raised on database layer errors are defined here.
"""
from fastapi import status

from plants_api.exceptions import PlantsApiError


class UnsatisfiedIdDependencyError(PlantsApiError):
    """
    Exception to raise on a (possible) foreign key named 'id' constraint violation.
    """

    def __init__(self, idx: int, table: str):
        """
        `table` refer to the database entities, `idx` is missing identifier given by user.
        """
        self.idx = idx
        self.table = table
        super().__init__()

    def __str__(self) -> str:
        return f"Broken dependency: there is no value '{self.idx}' in {self.table}.id"

    def get_status_code(self) -> int:
        return status.HTTP_400_BAD_REQUEST


class EntityNotFoundByIdError(PlantsApiError):
    """
    Exception to raise when user request is depending on an entity which cannot be found in the database by id.
    """

    def __init__(self, idx: int, table: str):
        """
        `table` refer to the database entities, `idx` is a identifier requested by user.
        """
        self.idx = idx
        self.table = table
        super().__init__()

    def __str__(self) -> str:
        return f"Entity not found: there is no value '{self.idx}' in {self.table}.id"

    def get_status_code(self) -> int:
        return status.HTTP_404_NOT_FOUND
