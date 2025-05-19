from fastapi.testclient import TestClient
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import warnings

warnings.filterwarnings(
    "ignore",
    message="'crypt' is deprecated",
    category=DeprecationWarning,
    module="passlib",
)

from app.main import app
from app.database import Base, get_db
from app import models, auth

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if TEST_DATABASE_URL:
    engine = create_engine(TEST_DATABASE_URL)
else:
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_signup_and_login():
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


def test_signup_success():
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


def test_login_success():
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
