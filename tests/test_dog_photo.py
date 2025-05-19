import re


def test_dog_photo_display_after_login(client):
    username = "doguser"
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

    response = client.get("/dogs")
    assert response.status_code == 200
    assert 'id="dog-photo"' in response.text
    assert 'id="spinner"' in response.text
    match = re.search(r'<img[^>]*id="dog-photo"[^>]*>', response.text)
    assert match, "dog photo img tag not found"
    tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', tag)
    assert src_match, "src attribute not found"
    assert src_match.group(1).startswith("https://")
    assert 'width="300"' in tag
    assert 'height="300"' in tag
