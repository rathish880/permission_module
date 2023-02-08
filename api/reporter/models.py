"""Contains ORM models."""
from sqlalchemy import Column, Identity, Integer, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP

from ..database import Base, engine


class Report(Base):
    """Mapping of `report` table."""

    __tablename__ = "reports"

    report_id = Column(Integer, Identity(always=True), primary_key=True)
    reported_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    reporter_group = Column(Text, nullable=False)
    details = Column(Text, nullable=False)


Base.metadata.create_all(engine)
