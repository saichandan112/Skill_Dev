"""Checklist template loading."""
import json
from copy import deepcopy
from modules.config import CONFIG_DIR


class ChecklistRepository:
    def __init__(self, template_path=None):
        self.template_path = template_path or CONFIG_DIR / "checklist_templates.json"
        self._templates = self._load()

    def _load(self):
        with open(self.template_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        if not isinstance(data, dict) or not data:
            raise ValueError("Checklist template file must contain a non-empty object.")
        for issue_type, steps in data.items():
            if not isinstance(steps, list) or not steps:
                raise ValueError(f"Checklist '{issue_type}' has no steps.")
            for item in steps:
                if not item.get("step") or not isinstance(item.get("ideas", []), list):
                    raise ValueError(f"Invalid step in checklist '{issue_type}'.")
        return data

    def issue_types(self):
        return sorted(self._templates.keys())

    def get(self, issue_type):
        if issue_type not in self._templates:
            raise KeyError(f"Unknown issue type: {issue_type}")
        return deepcopy(self._templates[issue_type])
