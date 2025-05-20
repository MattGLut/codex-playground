from conftest import login_helper


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

    # create user if not exists and log in
    login_helper(client, username, password)

    response = client.get("/account")
    assert response.status_code == 200
    assert '<input type="checkbox" id="toggle-dark"' in response.text
    assert 'applyDarkMode' in response.text
