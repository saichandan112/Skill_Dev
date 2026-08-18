import pyautogui
import os

def capture_screenshot(ticket_id, step_no):

    folder = f"screenshots/{ticket_id}"

    os.makedirs(folder, exist_ok=True)

    path = f"{folder}/step_{step_no}.png"

    screenshot = pyautogui.screenshot()

    screenshot.save(path)

    return path