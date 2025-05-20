from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)


class Suggestion(Base):
    """User submitted suggestions."""

    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User")


class UserSettings(Base):
    """Per-user persistent settings."""

    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    dark_mode = Column(Boolean, default=False, nullable=False)
    detailed_forecast = Column(Boolean, default=False, nullable=False)
    preferred_city = Column(String, default="nashville", nullable=False)
    preferred_animal = Column(String, default="cat", nullable=False)

    user = relationship("User", backref="settings", uselist=False)
