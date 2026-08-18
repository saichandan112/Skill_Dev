"""Compatibility wrapper for screenshot capture."""
from modules.screenshot_manager import ScreenshotManager


def capture_screenshot(destination_directory, step_number, delay_seconds=3):
    return ScreenshotManager(destination_directory).capture_full_screen(step_number, delay_seconds)
