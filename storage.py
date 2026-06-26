import json
import os

FILE = os.path.join(os.path.dirname(__file__), "tasks.json")


def load():
    if not os.path.exists(FILE):
        return []
    with open(FILE) as f:
        return json.load(f)


def save(tasks):
    with open(FILE, "w") as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)
