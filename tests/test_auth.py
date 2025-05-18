from fastapi.testclient import TestClient
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
