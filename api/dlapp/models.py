"""Contains ORM models for dlapp"""
from sqlalchemy import Boolean, Column, Identity, Integer, Text, func, null, true
from sqlalchemy.dialects.postgresql import TIMESTAMP
from urllib3.exceptions import TimeoutStateError

from ..database import Base, engine


class Permission(Base):
    """Mapping of `permissions` table."""

    __tablename__ = "permissions"

    permission_id = Column(Integer, Identity(always=True), primary_key=True)
    user_name = Column(Text, nullable=False)
    user_group = Column(Text, nullable=False)
    permission_date = Column(TIMESTAMP(timezone=True), nullable=False)
    permission_time = Column(Text, nullable=False)
    requested_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    head_approved = Column(Boolean, nullable=True)
    dean_approved = Column(Boolean, nullable=True)
    approved_on = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default="epoch"
    )
    reason = Column(Text, nullable=False)


class UserInfo(Base):
    """Mapping of `userinfo` table"""

    __tablename__ = "userinfo"

    username = Column(Text, primary_key=True)
    token = Column(Text)


Base.metadata.create_all(engine)
