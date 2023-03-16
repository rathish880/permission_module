"""Contains Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel


class ReportDetails(BaseModel):
    """Report details sent by user."""

    period: int
    details: str


class Report(ReportDetails):
    """Generic report submitted by the user."""

    report_id: int
    reported_on: datetime
    reporter_group: str
    period: int
    details: str

    class Config:
        orm_mode = True
