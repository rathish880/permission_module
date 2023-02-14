"""Contains Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel


class PermissionDetails(BaseModel):
    """permission details sent by the user"""

    permission_date: datetime
    permission_time: str
    reason: str


class Permission(BaseModel):
    """permission requested by the user"""

    permission_id: int
    user_name: str
    user_group: str
    permission_date: datetime
    permission_time: str
    requested_on: datetime
    approved_on: datetime
    reason: str

    class Config:
        orm_mode = True
