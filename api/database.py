"""Contains database ORM."""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .settings import Settings

engine = create_engine(Settings.DATABASE_URL)
SessionLocal = sessionmaker(engine)
Base = declarative_base()
