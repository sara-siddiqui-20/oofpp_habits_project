# models.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict


def iso_date(d: date) -> str:
    return d.isoformat()


def parse_iso(s: str) -> date:
    return datetime.fromisoformat(s).date()


@dataclass
class Habit:
    name: str
    periodicity: str  # 'daily' or 'weekly'
    created: str = field(default_factory=lambda: iso_date(date.today()))
    completed_dates: List[str] = field(default_factory=list)  # ISO dates

    def mark_complete(self, on_date: date = None):
        """Mark this habit as complete on the given date (today by default)."""
        d = on_date or date.today()
        s = iso_date(d)
        if s not in self.completed_dates:
            self.completed_dates.append(s)
            self.completed_dates.sort()
        return True

    def get_completed_dates(self) -> List[date]:
        return [parse_iso(s) for s in self.completed_dates]

    def _daily_streaks(self) -> List[int]:
        """Return list of consecutive daily streak lengths (all runs)."""
        days = sorted(self.get_completed_dates())
        if not days:
            return []
        runs = []
        run = 1
        for i in range(1, len(days)):
            if (days[i] - days[i - 1]) == timedelta(days=1):
                run += 1
            else:
                runs.append(run)
                run = 1
        runs.append(run)
        return runs

    def _weekly_streaks(self) -> List[int]:
        """Return streak lengths in weeks (based on ISO week). A week is counted if any date in that week is completed."""
        days = sorted(self.get_completed_dates())
        if not days:
            return []
        # Convert to (year, iso_week)
        weeks = sorted({(d.isocalendar()[0], d.isocalendar()[1]) for d in days})
        runs = []
        run = 1
        for i in range(1, len(weeks)):
            prev_year, prev_week = weeks[i - 1]
            year, week = weeks[i]
            # Increase if consecutive week considering year boundary
            prev_week_next = prev_week + 1
            prev_year_next = prev_year
            # handle iso week overflow (week number can go up to 52/53)
            # simpler: compute monday date for each (year, week)
            # fallback: compute Monday date then compare by 7 days
            # We'll compute Monday for both weeks to compare
            from datetime import datetime as dt
            def monday_of_iso(year_w, week_w):
                return dt.strptime(f'{year_w}-W{week_w}-1', "%G-W%V-%u").date()
            prev_monday = monday_of_iso(prev_year, prev_week)
            cur_monday = monday_of_iso(year, week)
            if (cur_monday - prev_monday) == timedelta(weeks=1):
                run += 1
            else:
                runs.append(run)
                run = 1
        runs.append(run)
        return runs

    def longest_streak(self) -> int:
        """Return longest streak (int) depending on periodicity."""
        if self.periodicity.lower() == 'daily':
            runs = self._daily_streaks()
        else:
            runs = self._weekly_streaks()
        return max(runs) if runs else 0

    def current_streak(self) -> int:
        """Return current ongoing streak up to today."""
        today = date.today()
        days = sorted(self.get_completed_dates())
        if not days:
            return 0
        if self.periodicity.lower() == 'daily':
            # Walk backwards from last completion
            streak = 0
            last = days[-1]
            if (today - last).days > 1:
                # Last completed not today or yesterday -> check if last completion is today or yesterday
                # Current streak only valid if last completion is within current period
                # If last completion is today or yesterday, compute
                pass
            # Count consecutive days ending at last
            for i in range(len(days) - 1, -1, -1):
                if i == len(days) - 1:
                    streak = 1
                else:
                    if (days[i + 1] - days[i]) == timedelta(days=1):
                        streak += 1
                    else:
                        break
            # If last completed date is too far in past (gap to today >0), current streak is zero unless last is today
            # However typical definition: current streak counts until last completed date; if last completion was today or yesterday then fine.
            # We'll treat current streak as streak up to last completed date only (common in trackers).
            return streak
        else:
            # weekly
            weeks = sorted({(d.isocalendar()[0], d.isocalendar()[1]) for d in days})
            if not weeks:
                return 0
            streak = 1
            def monday_of_iso(year_w, week_w):
                from datetime import datetime as dt
                return dt.strptime(f'{year_w}-W{week_w}-1', "%G-W%V-%u").date()
            for i in range(len(weeks) - 1, 0, -1):
                cur_monday = monday_of_iso(weeks[i][0], weeks[i][1])
                prev_monday = monday_of_iso(weeks[i - 1][0], weeks[i - 1][1])
                if (cur_monday - prev_monday) == timedelta(weeks=1):
                    streak += 1
                else:
                    break
            return streak


@dataclass
class HabitManager:
    habits: Dict[str, Habit] = field(default_factory=dict)

    def add_habit(self, habit: Habit):
        if habit.name in self.habits:
            raise ValueError(f"Habit with name '{habit.name}' already exists.")
        self.habits[habit.name] = habit

    def remove_habit(self, name: str):
        if name in self.habits:
            del self.habits[name]
        else:
            raise KeyError(f"Habit '{name}' not found.")

    def get_all_habits(self) -> List[Habit]:
        return list(self.habits.values())

    def get_habits_by_periodicity(self, periodicity: str) -> List[Habit]:
        return [h for h in self.habits.values() if h.periodicity.lower() == periodicity.lower()]

    def get_longest_streak(self) -> int:
        longest = 0
        for h in self.habits.values():
            s = h.longest_streak()
            if s > longest:
                longest = s
        return longest

    def get_longest_streak_for(self, name: str) -> int:
        if name not in self.habits:
            raise KeyError(f"Habit '{name}' not found.")
        return self.habits[name].longest_streak()