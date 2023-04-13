"""Contains Pydantic schemas."""
from datetime import datetime
from datetime import date
from enum import StrEnum

from pydantic import BaseModel


class HodStatus(StrEnum):
    """HOD status of a Permission"""

    DIRECT = "Direct"
    DENIED = "Denied"
    PENDING = "Pending"
    FORWARD = "Forward"


class WardenStatus(StrEnum):
    """Warden status of a Permission"""

    APPROVED = "Approved"
    DENIED = "Denied"
    PENDING = "Pending"


class PermissionDetails(BaseModel):
    """permission details sent by the user"""

    from_date: datetime
    to_date: datetime
    reason: str


class UpdateStatus(BaseModel):
    """update permission status by hod, warden"""

    permission_id: int
    permission_status: str


class Permission(BaseModel):
    """permission requested by the user"""

    permission_id: int
    user_name: str
    user_group: str
    from_date: date
    to_date: str
    requested_on: datetime
    hod_status: str
    warden_status: str
    acted_on: datetime
    reason: str

    class Config:
        orm_mode = True
