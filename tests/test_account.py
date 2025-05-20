def login_helper(client, username, password):
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


def test_account_requires_login(client):
    response = client.get("/account", follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"].startswith("/login")
    assert "error=Please%20log%20in%20to%20access%20that%20page" in response.headers["location"]


def test_account_page_and_link(client):
    username = "settings"
    password = "secret"
    login_helper(client, username, password)

    response = client.get("/protected")
    assert response.status_code == 200
    assert '<a href="/account">' in response.text

    response = client.get("/account")
    assert response.status_code == 200
    assert '<div class="top-header">' in response.text
    assert 'Codex Playground' in response.text
    assert '<a href="/protected">Codex Playground</a>' in response.text
    assert "Account Settings" in response.text
    assert username in response.text
    assert '<div class="sidebar">' in response.text
    assert '<a href="/protected">Home</a>' not in response.text
    assert 'id="toggle-detailed"' in response.text
