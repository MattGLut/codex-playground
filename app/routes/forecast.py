from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
import httpx

from .. import models
from ..dependencies import get_current_user, templates

router = APIRouter()


@router.get("/forecast/nashville", response_class=HTMLResponse)
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


@router.get("/forecast/nashville/detailed", response_class=HTMLResponse)
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
