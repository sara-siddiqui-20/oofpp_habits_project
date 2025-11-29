# analytics.py
from functools import reduce
from typing import List
from models import Habit, HabitManager

def list_all_habits(mgr: HabitManager) -> List[str]:
    # return names using map
    return list(map(lambda h: h.name, mgr.get_all_habits()))

def habits_by_periodicity(mgr: HabitManager, period: str) -> List[str]:
    # filter then map
    filtered = filter(lambda h: h.periodicity.lower() == period.lower(), mgr.get_all_habits())
    return list(map(lambda h: h.name, filtered))

def longest_run_streak_all(mgr: HabitManager) -> int:
    # reduce over habits to find max longest streak
    def reducer(acc, h):
        return acc if acc >= h.longest_streak() else h.longest_streak()
    return reduce(reducer, mgr.get_all_habits(), 0)

def longest_run_streak_for(mgr: HabitManager, habit_name: str) -> int:
    # find the habit using filter and map, then reduce (or take first)
    matches = list(filter(lambda h: h.name == habit_name, mgr.get_all_habits()))
    if not matches:
        raise KeyError(f"Habit '{habit_name}' not found.")
    h = matches[0]
    return h.longest_streak()
