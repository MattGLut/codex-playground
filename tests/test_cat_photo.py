import re


def test_cat_photo_display_after_login(client):
    username = "catuser"
    password = "secret"

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

    response = client.get("/protected")
    assert response.status_code == 200
    assert 'id="cat-photo"' in response.text
    match = re.search(r'<img[^>]+id="cat-photo"[^>]+src="([^"]+)"', response.text)
    assert match, "cat photo img tag with src not found"
    assert match.group(1).startswith("https://cataas.com/cat?")
