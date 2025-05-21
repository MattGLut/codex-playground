from typing import Tuple

from .ai_animals import AnimalGenerator

ALLOWED_ANIMALS = ["cat", "dog", "turtle"]


class RandomAnimalHandler:
    """Generate URLs for AI animal photos."""

    def __init__(self) -> None:
        self.generator = AnimalGenerator()

    def get_animal_url(self, animal: str) -> Tuple[str, str]:
        """Return a tuple of (animal, url) for the requested animal."""
        animal = (animal or "cat").lower()
        if animal not in ALLOWED_ANIMALS:
            animal = "cat"
        url = self.generator.generate_image(animal)
        return animal, url
