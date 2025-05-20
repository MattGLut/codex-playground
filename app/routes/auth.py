from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from .. import auth, models
from ..database import get_db
from ..dependencies import templates

router = APIRouter()


@router.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@router.post("/signup")
def signup(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password = auth.get_password_hash(password)
    user = models.User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        url = "/login?error=Invalid%20credentials"
        return RedirectResponse(url=url, status_code=303)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/protected", status_code=303)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)
