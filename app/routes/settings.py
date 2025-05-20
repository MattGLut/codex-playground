from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..dependencies import get_current_user
from ..user_settings import get_user_settings

router = APIRouter()


@router.get("/settings")
def read_settings(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_user_settings(db, user.id)
    return {
        "dark_mode": settings.dark_mode,
        "detailed_forecast": settings.detailed_forecast,
        "preferred_city": settings.preferred_city,
        "preferred_animal": settings.preferred_animal,
    }


@router.post("/settings")
def update_settings(
    dark_mode: bool | None = Form(None),
    detailed_forecast: bool | None = Form(None),
    preferred_city: str | None = Form(None),
    preferred_animal: str | None = Form(None),
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_user_settings(db, user.id)
    if dark_mode is not None:
        settings.dark_mode = dark_mode
    if detailed_forecast is not None:
        settings.detailed_forecast = detailed_forecast
    if preferred_city:
        settings.preferred_city = preferred_city
    if preferred_animal:
        settings.preferred_animal = preferred_animal
    db.commit()
    return {"success": True}
