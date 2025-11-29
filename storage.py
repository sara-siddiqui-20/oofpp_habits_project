# storage.py
import json
from typing import Dict
from models import Habit, HabitManager
from datetime import date

def habit_from_dict(d) -> Habit:
    return Habit(name=d["name"],
                 periodicity=d["periodicity"],
                 created=d.get("created", date.today().isoformat()),
                 completed_dates=d.get("completed_dates", []))


def load_from_file(path: str) -> HabitManager:
    mgr = HabitManager()
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for h in data.get("habits", []):
                habit = habit_from_dict(h)
                mgr.add_habit(habit)
    except FileNotFoundError:
        # return empty manager if no file exists
        pass
    return mgr


def save_to_file(mgr: HabitManager, path: str):
    data = {"habits": []}
    for h in mgr.get_all_habits():
        data["habits"].append({
            "name": h.name,
            "periodicity": h.periodicity,
            "created": h.created,
            "completed_dates": h.completed_dates
        })
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)