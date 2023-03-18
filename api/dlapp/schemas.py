"""Contains Pydantic schemas."""
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel


class Designation(StrEnum):
    """Designation of a user"""

    HEADS = "Heads"
    TEACHING = "Teaching"
    NON_TEACHING = "Non Teaching"


class DeanStatus(StrEnum):
    """Dean status of a Permission"""

    APPROVED = "Approved"
    DENIED = "Denied"
    PENDING = "Pending"


class HodStatus(StrEnum):
    """HOD status of a Permission"""

    DIRECT = "Direct"
    DENIED = "Denied"
    PENDING = "Pending"
    FORWARD = "Forward"


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
    hod_status: str
    dean_status: str
    approved_on: datetime
    reason: str

    class Config:
        orm_mode = True
