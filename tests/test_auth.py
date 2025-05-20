from app import models, auth
from conftest import TestingSessionLocal


def test_signup_and_login(client):
    # Sign up
    response = client.post(
        "/signup",
        data={"username": "alice", "password": "secret"},
        follow_redirects=False,
    )
    assert response.status_code == 303

    # Login
    response = client.post(
        "/login",
        data={"username": "alice", "password": "secret"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/protected"

    # Access protected page using cookies from login
    client.cookies.update(response.cookies)
    response = client.get("/protected")
    assert response.status_code == 200
    assert "Congrats! You signed in!" in response.text
    assert '<div class="top-header">' in response.text
    assert 'Codex Playground' in response.text
    assert '<a href="/protected">Codex Playground</a>' in response.text
    assert '<div class="sidebar">' in response.text
    assert '<a href="/protected">Home</a>' not in response.text
    assert '<a href="/forecast/nashville">' in response.text
def test_signup_success(client):
    response = client.post(
        "/signup",
        data={"username": "bob", "password": "password"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/login"

    with TestingSessionLocal() as db:
        user = db.query(models.User).filter(models.User.username == "bob").first()
        assert user is not None
        assert auth.verify_password("password", user.hashed_password)


def test_login_success(client):
    # Create user by signing up first
    client.post(
        "/signup",
        data={"username": "carol", "password": "topsecret"},
        follow_redirects=False,
    )

    response = client.post(
        "/login",
        data={"username": "carol", "password": "topsecret"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/protected"

    client.cookies.update(response.cookies)
    response = client.get("/protected")
    assert response.status_code == 200
    assert "Congrats! You signed in!" in response.text


def test_login_failure_redirect(client):
    client.post(
        "/signup",
        data={"username": "eve", "password": "secret"},
        follow_redirects=False,
    )

    response = client.post(
        "/login",
        data={"username": "eve", "password": "wrong"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")
    assert "error=Invalid%20credentials" in response.headers["location"]

    response = client.get(response.headers["location"])
    assert response.status_code == 200
    assert "Invalid credentials" in response.text
