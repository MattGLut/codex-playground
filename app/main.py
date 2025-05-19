from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.exception_handlers import http_exception_handler as fastapi_http_exception_handler
from fastapi.staticfiles import StaticFiles
import httpx
import time
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session

from . import auth, models, schemas
from .database import Base, engine, get_db, SessionLocal

Base.metadata.create_all(bind=engine)


def create_default_user(db: Session) -> None:
    """Create a default user if one does not already exist."""
    if not db.query(models.User).filter(models.User.username == "test").first():
        hashed = auth.get_password_hash("test")
        db.add(models.User(username="test", hashed_password=hashed))
        db.commit()


app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="secret")


@app.on_event("startup")
def startup_event() -> None:
    """Run startup tasks like creating the default user."""
    get_db_override = app.dependency_overrides.get(get_db, get_db)
    db_gen = get_db_override()
    db = next(db_gen)
    try:
        create_default_user(db)
    finally:
        try:
            next(db_gen)
        except StopIteration:
            pass

templates = Jinja2Templates(directory="templates")


app.mount("/static", StaticFiles(directory="static"), name="static")
# Redirect unauthorized access to login page


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Redirect unauthorized users to the login page with a warning."""
    if exc.status_code == status.HTTP_401_UNAUTHORIZED:
        url = app.url_path_for("login_form") + "?error=Please%20log%20in%20to%20access%20that%20page"
        return RedirectResponse(url=url, status_code=status.HTTP_303_SEE_OTHER)
    return await fastapi_http_exception_handler(request, exc)
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
    cat_url = f"https://cataas.com/cat?{int(time.time())}"
    return templates.TemplateResponse(
        request,
        "success.html",
        {"username": user.username, "cat_url": cat_url},
    )


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/forecast/nashville", response_class=HTMLResponse)
def nashville_forecast(
    request: Request, user: models.User = Depends(get_current_user)
):
    """Return Nashville's 7 day weather forecast from Open-Meteo as a web page."""
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
    data = response.json()
    forecast = list(
        zip(
            data["daily"]["time"],
            data["daily"]["temperature_2m_max"],
            data["daily"]["temperature_2m_min"],
        )
    )
    return templates.TemplateResponse(
        "forecast.html", {"request": request, "forecast": forecast}
    )


@app.get("/forecast/nashville/detailed", response_class=HTMLResponse)
def nashville_detailed_forecast(
    request: Request, user: models.User = Depends(get_current_user)
):
    """Return Nashville's 7 day detailed weather forecast as a web page."""
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": 36.1627,
            "longitude": -86.7816,
            "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
            "forecast_days": 7,
            "temperature_unit": "fahrenheit",
            "timezone": "America/Chicago",
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    weather_map = {
        0: "Clear",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        80: "Rain showers",
        95: "Thunderstorm",
    }
    forecast = [
        (
            date,
            weather_map.get(code, "Unknown"),
            tmax,
            tmin,
            precip,
        )
        for date, code, tmax, tmin, precip in zip(
            data["daily"]["time"],
            data["daily"]["weathercode"],
            data["daily"]["temperature_2m_max"],
            data["daily"]["temperature_2m_min"],
            data["daily"]["precipitation_probability_max"],
        )
    ]
    return templates.TemplateResponse(
        "forecast_detail.html", {"request": request, "forecast": forecast}
    )


@app.get("/dogs", response_class=HTMLResponse)
def random_dog(
    request: Request, user: models.User = Depends(get_current_user)
):
    """Display a random dog photo."""
    dog_url = f"https://placedog.net/500?{int(time.time())}"
    return templates.TemplateResponse(
        request,
        "dog.html",
        {"dog_url": dog_url},
    )


@app.get("/account", response_class=HTMLResponse)
def account_page(request: Request, user: models.User = Depends(get_current_user)):
    return templates.TemplateResponse(
        "account.html", {"request": request, "username": user.username}
    )
