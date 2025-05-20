from fastapi import Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import timezone, datetime
from zoneinfo import ZoneInfo

from .database import get_db
from . import models

templates = Jinja2Templates(directory="templates")

CENTRAL_TZ = ZoneInfo("America/Chicago")


def format_central(dt: datetime) -> str:
    """Format a datetime in the America/Chicago timezone."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(CENTRAL_TZ).strftime("%Y-%m-%d %H:%M")


templates.env.filters["format_central"] = format_central


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
