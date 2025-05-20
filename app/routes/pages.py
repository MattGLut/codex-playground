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
def protected(
    request: Request,
    animal: str = "cat",
    user: models.User = Depends(get_current_user),
):
    animal = animal.lower()
    if animal == "dog":
        url = f"https://placedog.net/500?{int(time.time())}"
    elif animal == "turtle":
        url = f"https://loremflickr.com/300/300/turtle?{int(time.time())}"
    else:
        animal = "cat"
        url = f"https://cataas.com/cat?{int(time.time())}"
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
