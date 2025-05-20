import pytest


def test_protected_redirects_to_login(client):
    response = client.get("/protected", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_dogs_redirects_to_login(client):
    response = client.get("/dogs", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_turtles_redirects_to_login(client):
    response = client.get("/turtles", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")
