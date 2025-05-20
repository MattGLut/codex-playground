def test_darkmode_toggle_not_in_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert 'id="toggle-dark"' not in response.text
    assert 'applyDarkMode' in response.text
    assert "localStorage.getItem('darkMode')" in response.text


def test_darkmode_toggle_not_in_signup_page(client):
    response = client.get("/signup")
    assert response.status_code == 200
    assert 'id="toggle-dark"' not in response.text
    assert 'applyDarkMode' in response.text


def test_darkmode_toggle_in_account_page_after_login(client):
    username = "darktoggle"
    password = "secret"

    # create user if not exists
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

    response = client.get("/account")
    assert response.status_code == 200
    assert '<input type="checkbox" id="toggle-dark"' in response.text
    assert 'applyDarkMode' in response.text
