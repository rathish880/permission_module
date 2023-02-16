"""Contains Pydantic schemas."""
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel
from sqlalchemy import Column


class Designation(StrEnum):
    """Designation of a user"""

    HEADS = "Heads"
    TEACHING = "Teaching"
    NON_TEACHING = "Non Teaching"


class PermissionDetails(BaseModel):
    """permission details sent by the user"""

    permission_date: datetime
    permission_time: str
    reason: str


class Permission(BaseModel):
    """permission requested by the user"""

    permission_id: Column[int]
    user_name: Column[str]
    user_group: Column[str]
    permission_date: Column[datetime]
    permission_time: Column[str]
    requested_on: Column[datetime]
    head_approved: Column[bool]
    dean_approved: Column[bool]
    approved_on: Column[datetime]
    reason: Column[str]

    class Config:
        orm_mode = True
