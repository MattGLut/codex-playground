from conftest import login_helper, TestingSessionLocal
from app import models
from app.dependencies import format_central


def test_suggestions_requires_login(client):
    response = client.get("/suggestions", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")


def test_suggestion_submission_and_display(client):
    # user1 submits a suggestion
    login_helper(client, "alice", "secret")
    response = client.post(
        "/suggestions",
        data={"content": "hello world"},
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["location"] == "/suggestions"

    with TestingSessionLocal() as db:
        suggestion = (
            db.query(models.Suggestion)
            .order_by(models.Suggestion.id.desc())
            .first()
        )
        timestamp_str = format_central(suggestion.timestamp)

    client.get("/logout")

    # user2 views the suggestion
    login_helper(client, "bob", "password")
    response = client.get("/suggestions")
    assert response.status_code == 200
    assert "hello world" in response.text
    assert "alice" in response.text
    assert timestamp_str in response.text
    assert "Suggestion Box" in response.text
    assert '<a href="/suggestions">Suggestion Box</a>' in response.text
    assert '<div class="suggestion-container">' in response.text
