"""Configuration loader and path resolution."""
import json
import os
import sys
from pathlib import Path


def application_base() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


BASE_DIR = application_base()
CONFIG_DIR = BASE_DIR / "config"


def load_app_config() -> dict:
    with open(CONFIG_DIR / "app_config.json", "r", encoding="utf-8") as handle:
        return json.load(handle)


def resolve_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else BASE_DIR / path
