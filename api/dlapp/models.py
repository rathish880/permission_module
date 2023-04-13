"""Contains ORM models for dlapp - staff"""
from sqlalchemy import Column, Text
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base, engine


class UserInfo(Base):
    """Mapping of `userinfo` table"""

    __tablename__ = "userinfo"

    user_id = Column(UUID(as_uuid=True), primary_key=True)
    token = Column(Text)


Base.metadata.create_all(engine)
