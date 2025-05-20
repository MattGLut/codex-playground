import pytest


def test_protected_redirects_to_login(client):
    response = client.get("/protected", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_protected_dog_requires_login(client):
    response = client.get("/protected?animal=dog", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_protected_turtle_requires_login(client):
    response = client.get("/protected?animal=turtle", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")
