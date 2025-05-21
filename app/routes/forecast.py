from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
import httpx
from sqlalchemy.orm import Session
from .. import models
from ..dependencies import get_current_user, templates
from ..database import get_db
from ..user_settings import get_user_settings

router = APIRouter()

WEATHER_MAP = {
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

CITIES = {
    "nashville": {
        "name": "Nashville",
        "latitude": 36.1627,
        "longitude": -86.7816,
    },
    "holts-summit": {
        "name": "Holts Summit",
        "latitude": 38.95,
        "longitude": -92.12,
    },
}


def _get_forecast_data(city: dict, detailed: bool):
    daily = "temperature_2m_max,temperature_2m_min"
    if detailed:
        daily = (
            "weathercode,temperature_2m_max,temperature_2m_min," "precipitation_probability_max"
        )
    response = httpx.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": city["latitude"],
            "longitude": city["longitude"],
            "daily": daily,
            "forecast_days": 7,
            "temperature_unit": "fahrenheit",
            "timezone": "America/Chicago",
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def _render_forecast(request: Request, slug: str, detailed: bool, user: models.User, db: Session):
    city = CITIES[slug]
    settings = get_user_settings(db, user.id)
    settings.preferred_city = slug
    settings.detailed_forecast = detailed
    db.commit()
    try:
        data = _get_forecast_data(city, detailed)
    except httpx.HTTPError:
        return HTMLResponse(
            "Failed to fetch forecast data. Please try again later.",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )

    if detailed:
        forecast = [
            (
                date,
                WEATHER_MAP.get(code, "Unknown"),
                tmax,
                tmin,
                precip,
            )
            for date, code, tmax, tmin, precip in zip(
                data["daily"]["time"],
                data["daily"].get("weathercode", []),
                data["daily"]["temperature_2m_max"],
                data["daily"]["temperature_2m_min"],
                data["daily"].get("precipitation_probability_max", []),
            )
        ]
        template = "forecast_detail.html"
    else:
        forecast = list(
            zip(
                data["daily"]["time"],
                data["daily"]["temperature_2m_max"],
                data["daily"]["temperature_2m_min"],
            )
        )
        template = "forecast.html"
    today = forecast[0][0] if forecast else ""

    return templates.TemplateResponse(
        template,
        {
            "request": request,
            "forecast": forecast,
            "city_name": city["name"],
            "slug": slug,
            "today": today,
            "cities": {k: v["name"] for k, v in CITIES.items()},
            "detailed": settings.detailed_forecast,
            "dark_mode": settings.dark_mode,
        },
    )


@router.get("/forecast/nashville", response_class=HTMLResponse)
def nashville_forecast(
    request: Request,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return Nashville's 7 day weather forecast as a web page."""
    return _render_forecast(request, "nashville", False, user, db)


@router.get("/forecast/nashville/detailed", response_class=HTMLResponse)
def nashville_detailed_forecast(
    request: Request,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return Nashville's 7 day detailed weather forecast as a web page."""
    return _render_forecast(request, "nashville", True, user, db)


@router.get("/forecast/holts-summit", response_class=HTMLResponse)
def holts_summit_forecast(
    request: Request,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return Holts Summit's 7 day weather forecast as a web page."""
    return _render_forecast(request, "holts-summit", False, user, db)


@router.get("/forecast/holts-summit/detailed", response_class=HTMLResponse)
def holts_summit_detailed_forecast(
    request: Request,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return Holts Summit's 7 day detailed weather forecast as a web page."""
    return _render_forecast(request, "holts-summit", True, user, db)
