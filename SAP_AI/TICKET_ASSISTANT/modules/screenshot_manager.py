"""Evidence import, optional capture, validation, and safe naming."""
from pathlib import Path
from shutil import copy2
from PIL import Image


class ScreenshotManager:
    ALLOWED = {'.png', '.jpg', '.jpeg'}

    def __init__(self, screenshot_dir):
        self.screenshot_dir = Path(screenshot_dir)
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def target(self, step_number):
        return self.screenshot_dir / f"step_{step_number:02d}.png"

    def import_sanitized(self, source, step_number):
        source = Path(source)
        if source.suffix.lower() not in self.ALLOWED or not source.exists():
            raise ValueError("Select an existing PNG or JPEG image.")
        destination = self.target(step_number)
        with Image.open(source) as image:
            image.convert('RGB').save(destination, 'PNG')
        self.validate(destination)
        return destination

    def capture_full_screen(self, step_number, delay_seconds=3):
        import time
        import pyautogui
        time.sleep(max(0, int(delay_seconds)))
        destination = self.target(step_number)
        pyautogui.screenshot(str(destination))
        self.validate(destination)
        return destination

    @staticmethod
    def validate(path):
        path = Path(path)
        if not path.exists() or path.stat().st_size == 0:
            raise ValueError("Evidence image was not created.")
        with Image.open(path) as image:
            image.verify()
        return True
