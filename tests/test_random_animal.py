from app.random_animal import RandomAnimalHandler
from app.ai_animals import AnimalGenerator


def _mock_image(self, animal: str) -> str:
    return f"/static/generated/{animal}_img.png"


def test_dog_url(monkeypatch):
    monkeypatch.setattr(AnimalGenerator, "generate_image", _mock_image)
    handler = RandomAnimalHandler()
    animal, url = handler.get_animal_url("dog")
    assert animal == "dog"
    assert url == "/static/generated/dog_img.png"


def test_turtle_url(monkeypatch):
    monkeypatch.setattr(AnimalGenerator, "generate_image", _mock_image)
    handler = RandomAnimalHandler()
    animal, url = handler.get_animal_url("turtle")
    assert animal == "turtle"
    assert url == "/static/generated/turtle_img.png"


def test_default_cat(monkeypatch):
    monkeypatch.setattr(AnimalGenerator, "generate_image", _mock_image)
    handler = RandomAnimalHandler()
    animal, url = handler.get_animal_url("badger")
    assert animal == "cat"
    assert url == "/static/generated/cat_img.png"
