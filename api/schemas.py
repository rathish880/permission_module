"""Contains Pydantic schemas."""
from enum import StrEnum

from pydantic import BaseModel


class Role(StrEnum):
    """Role mappings for a user."""

    _INTERNAL = "internal"
    DEAN = "dean"
    STUDENT = "student"
    STAFF = "staff"
    TEACHER = "teacher"
    HR = "hr"

    @classmethod
    def _missing_(cls, _role: str):
        """Default value for internal roles."""
        return Role._INTERNAL


class User(BaseModel):
    """A generic user model."""

    user_id: str
    name: str
    groups: list[str]
    roles: list[Role]
