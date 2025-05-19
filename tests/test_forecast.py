import httpx


def test_nashville_forecast_endpoint(monkeypatch, client):
    expected = {
        "daily": {
            "time": ["2025-05-20", "2025-05-21", "2025-05-22", "2025-05-23", "2025-05-24", "2025-05-25", "2025-05-26"],
            "temperature_2m_max": [70, 71, 72, 73, 74, 75, 76],
            "temperature_2m_min": [50, 51, 52, 53, 54, 55, 56],
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
        assert params["latitude"] == 36.1627
        assert params["longitude"] == -86.7816
        return MockResponse(expected)

    monkeypatch.setattr(httpx, "get", mock_get)

    # create and login user
    username = "weather"
    password = "secret"
    client.post(
        "/signup",
        data={"username": username, "password": password},
        follow_redirects=False,
    )

    response = client.post(
        "/login",
        data={"username": username, "password": password},
        follow_redirects=False,
    )
    assert response.status_code == 303
    client.cookies.update(response.cookies)

    response = client.get("/forecast/nashville")
    assert response.status_code == 200
    assert "Nashville 7-Day Forecast" in response.text
    assert expected["daily"]["time"][0] in response.text


def test_nashville_forecast_requires_login(monkeypatch, client):
    """Ensure the forecast endpoint is protected."""

    def fail_get(*args, **kwargs):
        raise AssertionError("httpx.get should not be called when unauthorized")

    monkeypatch.setattr(httpx, "get", fail_get)

    response = client.get("/forecast/nashville")
    assert response.status_code == 401
