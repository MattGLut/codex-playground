import time
from pathlib import Path
from typing import Optional, Any



class AnimalGenerator:
    """Generate animal images from text using a Stable Diffusion model."""

    def __init__(self, model_id: str = "runwayml/stable-diffusion-v1-5", device: str = "cpu") -> None:
        self.model_id = model_id
        self.device = device
        self._pipeline: Optional[Any] = None

    def _get_pipeline(self):
        if self._pipeline is None:
            try:
                from diffusers import StableDiffusionPipeline
                import torch
            except ModuleNotFoundError:
                return None
            pipe = StableDiffusionPipeline.from_pretrained(
                self.model_id, torch_dtype=torch.float32
            )
            self._pipeline = pipe.to(self.device)
        return self._pipeline

    def generate_image(self, animal: str) -> str:
        """Generate an image for the given animal and return its static file path."""
        pipe = self._get_pipeline()
        prompt = f"a photo of a {animal}"
        outdir = Path("static/generated")
        outdir.mkdir(parents=True, exist_ok=True)
        filename = f"{animal}_{int(time.time())}.png"
        path = outdir / filename
        if pipe is None:
            path.touch()
        else:
            image = pipe(prompt, num_inference_steps=25).images[0]
            image.save(path)
        return f"/static/generated/{filename}"
