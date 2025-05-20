from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse

from ..random_animal import RandomAnimalHandler

from .. import models
from ..dependencies import get_current_user, templates

_animal_handler = RandomAnimalHandler()

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/protected", response_class=HTMLResponse)
def protected(
    request: Request,
    animal: str = "cat",
    user: models.User = Depends(get_current_user),
):
    animal, url = _animal_handler.get_animal_url(animal)
    return templates.TemplateResponse(
        "success.html",
        {
            "request": request,
            "username": user.username,
            "animal_url": url,
            "animal": animal,
        },
    )




@router.get("/account", response_class=HTMLResponse)
def account_page(request: Request, user: models.User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "account.html", {"request": request, "username": user.username}
    )
