import json
from pathlib import Path

from app.models.user import User

USERS_FILE = Path("users.json")

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, "r", encoding="utf-8") as file:
            return [User(**user) for user in json.load(file)]
    return []

