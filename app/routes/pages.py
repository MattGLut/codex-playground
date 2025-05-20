from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
import time

from .. import models
from ..dependencies import get_current_user, templates

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/protected", response_class=HTMLResponse)
def protected(request: Request, user: models.User = Depends(get_current_user)):
    cat_url = f"https://cataas.com/cat?{int(time.time())}"
    return templates.TemplateResponse(
        "success.html",
        {"request": request, "username": user.username, "cat_url": cat_url},
    )


@router.get("/dogs", response_class=HTMLResponse)
def random_dog(request: Request, user: models.User = Depends(get_current_user)):
    dog_url = f"https://placedog.net/500?{int(time.time())}"
    return templates.TemplateResponse(
        "dog.html",
        {"request": request, "dog_url": dog_url},
    )


@router.get("/turtles", response_class=HTMLResponse)
def random_turtle(
    request: Request, user: models.User = Depends(get_current_user)
):
    turtle_url = f"https://source.unsplash.com/300x300/?turtle&{int(time.time())}"
    return templates.TemplateResponse(
        "turtle.html",
        {"request": request, "turtle_url": turtle_url},
    )


@router.get("/account", response_class=HTMLResponse)
def account_page(request: Request, user: models.User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "account.html", {"request": request, "username": user.username}
    )
