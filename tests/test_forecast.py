import httpx
import pytest
from conftest import login_helper
from app.routes.forecast import CITIES


@pytest.mark.parametrize(
    "slug,lat,lon",
    [
        ("nashville", 36.1627, -86.7816),
        ("holts-summit", 38.95, -92.12),
    ],
)
def test_forecast_endpoint(monkeypatch, client, slug, lat, lon):
    expected = {
        "daily": {
            "time": ["2025-05-20"],
            "temperature_2m_max": [70],
            "temperature_2m_min": [50],
        }
    }

    class MockResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            pass

    def mock_get(url, params=None, timeout=None):
        assert url == "https://api.open-meteo.com/v1/forecast"
        assert params["latitude"] == lat
        assert params["longitude"] == lon
        return MockResponse(expected)

    monkeypatch.setattr(httpx, "get", mock_get)

    username = slug.replace("-", "")
    password = "secret"
    login_helper(client, username, password)

    response = client.get(f"/forecast/{slug}")
    assert response.status_code == 200
    assert f"{CITIES[slug]['name']} 7-Day Forecast" in response.text
    assert expected["daily"]["time"][0] in response.text
    assert 'id="city-select"' in response.text
    for s in CITIES:
        assert f'<option value="{s}"' in response.text
    assert f'<option value="{slug}" selected' in response.text
    assert "detailedForecast" in response.text


@pytest.mark.parametrize(
    "slug,lat,lon",
    [
        ("nashville", 36.1627, -86.7816),
        ("holts-summit", 38.95, -92.12),
    ],
)
def test_detailed_forecast_endpoint(monkeypatch, client, slug, lat, lon):
    expected = {
        "daily": {
            "time": ["2025-05-20"],
            "weathercode": [2],
            "temperature_2m_max": [70],
            "temperature_2m_min": [50],
            "precipitation_probability_max": [30],
        }
    }

    class MockResponse:
        def __init__(self, data):
            self._data = data

        def json(self):
            return self._data

        def raise_for_status(self):
            pass

    def mock_get(url, params=None, timeout=None):
        assert url == "https://api.open-meteo.com/v1/forecast"
        assert params["latitude"] == lat
        assert params["longitude"] == lon
        assert "weathercode" in params["daily"]
        return MockResponse(expected)

    monkeypatch.setattr(httpx, "get", mock_get)

    username = f"detail{slug.replace('-', '')}"
    password = "secret"
    login_helper(client, username, password)

    response = client.get(f"/forecast/{slug}/detailed")
    assert response.status_code == 200
    assert f"{CITIES[slug]['name']} Detailed Forecast" in response.text
    assert expected["daily"]["time"][0] in response.text
    assert "Partly cloudy" in response.text
    assert "30%" in response.text
    assert 'id="city-select"' in response.text
    assert "detailedForecast" in response.text


@pytest.mark.parametrize("path", [
    "/forecast/nashville",
    "/forecast/holts-summit",
    "/forecast/nashville/detailed",
    "/forecast/holts-summit/detailed",
])
def test_forecast_requires_login(monkeypatch, client, path):
    def fail_get(*args, **kwargs):
        raise AssertionError("httpx.get should not be called when unauthorized")

    monkeypatch.setattr(httpx, "get", fail_get)

    response = client.get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")
    assert "error=Please%20log%20in%20to%20access%20that%20page" in response.headers["location"]


@pytest.mark.parametrize("slug", ["nashville", "holts-summit"])
def test_forecast_httpx_error(monkeypatch, client, slug):
    def mock_get(*args, **kwargs):
        raise httpx.HTTPError("boom")

    monkeypatch.setattr(httpx, "get", mock_get)

    username = f"err{slug.replace('-', '')}"
    password = "secret"
    login_helper(client, username, password)

    response = client.get(f"/forecast/{slug}")
    assert response.status_code == 502
    assert "Failed to fetch forecast data" in response.text


@pytest.mark.parametrize("slug", ["nashville", "holts-summit"])
def test_detailed_forecast_httpx_error(monkeypatch, client, slug):
    def mock_get(*args, **kwargs):
        raise httpx.HTTPError("boom")

    monkeypatch.setattr(httpx, "get", mock_get)

    username = f"errdetail{slug.replace('-', '')}"
    password = "secret"
    login_helper(client, username, password)

    response = client.get(f"/forecast/{slug}/detailed")
    assert response.status_code == 502
    assert "Failed to fetch forecast data" in response.text
