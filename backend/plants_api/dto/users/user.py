"""
User DTO is defined here.
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class User:
    """
    Full User data transfer object, but without password_hash.
    """

    id: int  # pylint: disable=invalid-name
    email: str
    is_approved: bool
    registered_at: datetime
    device: str | None = None

    def __str__(self) -> str:
        return f"(id={self.id}, email: {self.email}, device={self.device})"
