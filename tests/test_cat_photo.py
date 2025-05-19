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
    match = re.search(r'<img[^>]*id="cat-photo"[^>]*>', response.text)
    assert match, "cat photo img tag not found"
    tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', tag)
    assert src_match, "src attribute not found"
    assert src_match.group(1).startswith("https://cataas.com/cat?")
    assert 'width="300"' in tag
    assert 'height="300"' in tag
