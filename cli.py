# cli.py
import sys
from datetime import datetime, date

from models import Habit, HabitManager
from storage import load_from_file, save_to_file
from analytics import (
    list_all_habits,
    habits_by_periodicity,
    longest_run_streak_all,
    longest_run_streak_for
)

# Default data file
DATA_FILE = "sample_data.json"


def prompt_menu():
    print("\n=== Habit Tracker ===")
    print("1) List all habits")
    print("2) List habits by periodicity (daily/weekly)")
    print("3) Add a habit")
    print("4) Remove a habit")
    print("5) Mark habit as completed")
    print("6) Show longest streak (all habits)")
    print("7) Show longest streak (specific habit)")
    print("8) Exit (save and quit)")
    return input("Choose an option: ").strip()


def run_cli(data_file: str = DATA_FILE):
    mgr = load_from_file(data_file)

    while True:
        choice = prompt_menu()

        # List all habits
        if choice == "1":
            habits = list_all_habits(mgr)
            if not habits:
                print("No habits tracked yet.")
            else:
                print("\nYour habits:")
                for h in habits:
                    print("-", h)

        # List habits by periodicity
        elif choice == "2":
            p = input("Enter periodicity (daily/weekly): ").strip()
            filtered = habits_by_periodicity(mgr, p)
            if not filtered:
                print(f"No habits found for periodicity '{p}'.")
            else:
                print("\nMatching habits:")
                for h in filtered:
                    print("-", h)

        # Add a habit
        elif choice == "3":
            name = input("Habit name: ").strip()
            p = input("Periodicity (daily/weekly): ").strip()

            h = Habit(name=name, periodicity=p)
            try:
                mgr.add_habit(h)
                print("Habit added successfully.")
            except ValueError as e:
                print("Error:", e)

        # Remove a habit
        elif choice == "4":
            name = input("Habit name to remove: ").strip()
            try:
                mgr.remove_habit(name)
                print("Habit removed.")
            except KeyError as e:
                print("Error:", e)

        # Mark habit complete
        elif choice == "5":
            name = input("Habit name to mark complete: ").strip()

            if name not in mgr.habits:
                print("Habit not found.")
                continue

            date_input = input("Date (YYYY-MM-DD) or ENTER for today: ").strip()
            if date_input:
                try:
                    d = datetime.fromisoformat(date_input).date()
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
                    continue
            else:
                d = date.today()

            mgr.habits[name].mark_complete(d)
            print(f"Habit '{name}' marked complete on {d.isoformat()}.")

        # Longest streak across all habits
        elif choice == "6":
            streak = longest_run_streak_all(mgr)
            print("Longest streak (any habit):", streak)

        # Longest streak for a specific habit
        elif choice == "7":
            name = input("Habit name: ").strip()
            try:
                streak = longest_run_streak_for(mgr, name)
                print(f"Longest streak for '{name}': {streak}")
            except KeyError as e:
                print("Error:", e)

        # Exit and save
        elif choice == "8":
            save_to_file(mgr, data_file)
            print(f"Progress saved to {data_file}. Exiting program.")
            sys.exit(0)

        else:
            print("Invalid choice. Try again.")
        
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Habit Tracker CLI")
    parser.add_argument("--data", "-d", default=None, help="Path to data file")

    args = parser.parse_args()

    file_to_use = args.data if args.data else DATA_FILE

    run_cli(file_to_use)