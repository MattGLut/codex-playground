import time
from typing import Tuple


class RandomAnimalHandler:
    """Generate URLs for random animal photos."""

    def get_animal_url(self, animal: str) -> Tuple[str, str]:
        """Return a tuple of (animal, url) for the requested animal."""
        animal = (animal or "cat").lower()
        ts = int(time.time())
        if animal == "dog":
            url = f"https://placedog.net/500?{ts}"
        elif animal == "turtle":
            # Use Unsplash to reliably fetch a random turtle photo
            url = f"https://source.unsplash.com/300x300/?turtle&{ts}"
        else:
            animal = "cat"
            url = f"https://cataas.com/cat?{ts}"
        return animal, url
