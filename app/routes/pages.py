from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from ..random_animal import ALLOWED_ANIMALS, RandomAnimalHandler

from .. import models
from ..dependencies import get_current_user, templates
from ..database import get_db
from sqlalchemy.orm import Session
from ..user_settings import get_user_settings

_animal_handler = RandomAnimalHandler()

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/protected", response_class=HTMLResponse)
def protected(
    request: Request,
    animal: str | None = None,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_user_settings(db, user.id)
    selected = animal or settings.preferred_animal
    if selected not in ALLOWED_ANIMALS:
        selected = "cat"
    if animal:
        settings.preferred_animal = selected
        db.commit()
    animal, url = _animal_handler.get_animal_url(selected)
    settings.preferred_animal = animal
    db.commit()
    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "username": user.username,
            "animal_url": url,
            "animal": animal,
            "dark_mode": settings.dark_mode,
            "detailed": settings.detailed_forecast,
            "preferred_animal": settings.preferred_animal,
            "allowed_animals": ALLOWED_ANIMALS,
        },
    )




@router.get("/account", response_class=HTMLResponse)
def account_page(
    request: Request,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings = get_user_settings(db, user.id)
    return templates.TemplateResponse(
        "account.html",
        {
            "request": request,
            "username": user.username,
            "dark_mode": settings.dark_mode,
            "detailed": settings.detailed_forecast,
        },
    )
