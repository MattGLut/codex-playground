import httpx
from conftest import login_helper, TestingSessionLocal
from app import models


def _get_settings(username):
    with TestingSessionLocal() as db:
        user = db.query(models.User).filter(models.User.username == username).first()
        return db.query(models.UserSettings).filter(models.UserSettings.user_id == user.id).first()


def test_settings_created_on_signup(client):
    username = "prefuser"
    password = "secret"
    login_helper(client, username, password)
    settings = _get_settings(username)
    assert settings is not None
    assert settings.preferred_animal == "cat"
    assert settings.preferred_city == "nashville"
    assert settings.detailed_forecast is False
    assert settings.dark_mode is False


def test_settings_persist(client):
    username = "prefs"
    password = "secret"
    login_helper(client, username, password)
    client.get("/protected?animal=dog")
    client.get("/forecast/holts-summit/detailed")
    settings = _get_settings(username)
    assert settings.preferred_animal == "dog"
    assert settings.preferred_city == "holts-summit"
    assert settings.detailed_forecast is True
    client.get("/logout")
    login_helper(client, username, password)
    response = client.get("/account")
    assert 'id="toggle-detailed" checked' in response.text


def test_forecast_respects_saved_setting(monkeypatch, client):
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
        assert "weathercode" in params["daily"]
        return MockResponse(expected)

    monkeypatch.setattr(httpx, "get", mock_get)

    username = "detailpref"
    password = "secret"
    login_helper(client, username, password)

    client.post(
        "/settings",
        data={"detailed_forecast": True},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    response = client.get("/forecast/nashville")
    assert response.status_code == 200
    assert "Nashville Detailed Forecast" in response.text
