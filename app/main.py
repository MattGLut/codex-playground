from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
import httpx
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")

templates = Jinja2Templates(directory="templates")


# Dependency


def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user


@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse(request, "signup.html")


@app.post("/signup")
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


@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    error = request.query_params.get("error")
    return templates.TemplateResponse(request, "login.html", {"error": error})


@app.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        url = app.url_path_for("login_form") + "?error=Invalid%20credentials"
        return RedirectResponse(url=url, status_code=303)
    request.session["user_id"] = user.id
    return RedirectResponse(url="/protected", status_code=303)


@app.get("/protected", response_class=HTMLResponse)
def protected(request: Request, user: models.User = Depends(get_current_user)):
    return templates.TemplateResponse(
        request,
        "success.html",
        {"username": user.username},
    )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/forecast/nashville")
def nashville_forecast():
    """Return Nashville's 7 day weather forecast from Open-Meteo."""
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 36.1627,
            "longitude": -86.7816,
            "daily": "temperature_2m_max,temperature_2m_min",
            "forecast_days": 7,
            "temperature_unit": "fahrenheit",
            "timezone": "America/Chicago",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
