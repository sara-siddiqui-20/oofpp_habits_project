# tests/test_habits.py
import os
import tempfile
from datetime import date, timedelta
from models import Habit, HabitManager
from storage import save_to_file, load_from_file
from analytics import list_all_habits, habits_by_periodicity, longest_run_streak_all

def test_habit_mark_and_streaks():
    h = Habit(name="Test", periodicity="daily")
    today = date.today()
    h.mark_complete(today - timedelta(days=2))
    h.mark_complete(today - timedelta(days=1))
    h.mark_complete(today)
    assert h.longest_streak() >= 3
    assert h.current_streak() >= 1

def test_manager_storage(tmp_path):
    mgr = HabitManager()
    h1 = Habit(name="A", periodicity="daily")
    h1.mark_complete(date.today())
    mgr.add_habit(h1)
    filep = tmp_path / "d.json"
    save_to_file(mgr, str(filep))
    loaded = load_from_file(str(filep))
    assert "A" in loaded.habits

def test_analytics_functions():
    mgr = HabitManager()
    mgr.add_habit(Habit(name="a", periodicity="daily"))
    mgr.add_habit(Habit(name="b", periodicity="weekly"))
    assert "a" in list_all_habits(mgr)
    assert "b" in habits_by_periodicity(mgr, "weekly")
    assert longest_run_streak_all(mgr) == 0