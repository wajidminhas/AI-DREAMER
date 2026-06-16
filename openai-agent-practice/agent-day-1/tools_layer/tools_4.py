


import json
import os
from agents import function_tool

MEMORY_FILE = "user_memory.json"


def _load(user_id: str) -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
        return data.get(user_id, {})
    return {}


def _save(user_id: str, memory: dict):
    data = {}
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    data[user_id] = memory
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)


@function_tool
def remember_preference(user_id: str, preference: str) -> str:
    """Save a user preference to persistent memory."""
    mem = _load(user_id)
    mem.setdefault("preferences", []).append(preference)
    _save(user_id, mem)
    return f"Saved preference: {preference}"


@function_tool
def recall_preferences(user_id: str) -> str:
    """Retrieve all saved preferences for a user."""
    mem = _load(user_id)
    prefs = mem.get("preferences", [])
    if prefs:
        return f"User preferences: {prefs}"
    return "No preferences saved yet."