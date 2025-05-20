from app.random_animal import RandomAnimalHandler


def test_dog_url(monkeypatch):
    handler = RandomAnimalHandler()
    monkeypatch.setattr("time.time", lambda: 123)
    animal, url = handler.get_animal_url("dog")
    assert animal == "dog"
    assert url == "https://placedog.net/500?123"


def test_turtle_url(monkeypatch):
    handler = RandomAnimalHandler()
    monkeypatch.setattr("time.time", lambda: 456)
    animal, url = handler.get_animal_url("turtle")
    assert animal == "turtle"
    assert url == "https://loremflickr.com/300/300/turtle?456"


def test_default_cat(monkeypatch):
    handler = RandomAnimalHandler()
    monkeypatch.setattr("time.time", lambda: 789)
    animal, url = handler.get_animal_url("badger")
    assert animal == "cat"
    assert url == "https://cataas.com/cat?789"
