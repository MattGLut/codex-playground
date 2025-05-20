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
