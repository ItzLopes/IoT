import os
from typing import Optional

class StorageService:
    def __init__(self, base_dir: str):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_image(self, name: str, image_data: bytes) -> Optional[str]:
        person_dir = os.path.join(self.base_dir, name)
        os.makedirs(person_dir, exist_ok=True)
        count = len(os.listdir(person_dir))
        filepath = os.path.join(person_dir, f"{count}.jpg")
        with open(filepath, "wb") as f:
            f.write(image_data)
        return filepath