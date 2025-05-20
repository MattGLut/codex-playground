from app import models, auth
from conftest import TestingSessionLocal


def test_default_user_exists(client):
    # Verify the default user was created at startup
    with TestingSessionLocal() as db:
        user = db.query(models.User).filter(models.User.username == "test").first()
        assert user is not None
        assert auth.verify_password("test", user.hashed_password)

    # Ensure login works with default credentials
    response = client.post(
        "/login",
        data={"username": "test", "password": "test"},
        follow_redirects=False,
    )
    assert response.status_code == 303
