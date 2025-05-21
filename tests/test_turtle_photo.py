import re
from conftest import login_helper


def test_turtle_photo_display_after_login(client):
    username = "turtleuser"
    password = "secret"

    login_helper(client, username, password)

    response = client.get("/protected?animal=turtle")
    assert response.status_code == 200
    assert 'id="animal-photo"' in response.text
    assert 'id="spinner"' in response.text
    match = re.search(r'<img[^>]*id="animal-photo"[^>]*>', response.text)
    assert match, "turtle photo img tag not found"
    tag = match.group(0)
    src_match = re.search(r'src="([^"]+)"', tag)
    assert src_match, "src attribute not found"
    assert src_match.group(1).startswith("/static/generated/")
    assert 'width="300"' in tag
    assert 'height="300"' in tag
