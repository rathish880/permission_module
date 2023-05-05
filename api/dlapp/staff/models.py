"""Contains ORM models for dlapp - staff"""
from sqlalchemy import Column, Identity, Integer, Date, Text, func
from sqlalchemy.dialects.postgresql import TIMESTAMP, ENUM, UUID

from .schemas import HodStatus, DeanStatus
from ...database import Base, engine


class Permission(Base):
    """Mapping of `permissions` table."""

    __tablename__ = "permissions"

    permission_id = Column(Integer, Identity(always=True), primary_key=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    user_group = Column(Text, nullable=False)
    permission_date = Column(Date, nullable=False, server_default=func.current_date())
    permission_time = Column(Text, nullable=False)
    requested_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    hod_status = Column(ENUM(*(status.value for status in HodStatus), name="HodStatus"))
    dean_status = Column(
        ENUM(*(status.value for status in DeanStatus), name="DeanStatus")
    )
    acted_on = Column(TIMESTAMP(timezone=True), nullable=False, server_default="epoch")
    reason = Column(Text, nullable=False)

class UserInfo(Base):
    
    __tablename__="user_info"
    user_id = Column(UUID(as_uuid=True), nullable=False)
    token = Column(Text, nullable=False)


Base.metadata.create_all(engine)
