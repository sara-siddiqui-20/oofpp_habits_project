# Habit Tracker (OO + Functional Python)

## Requirements
- Python 3.7+
- (recommended) virtualenv

## Install
1. Clone repository
2. (Optional) create virtual env:
   python -m venv venv
   source venv/bin/activate  # linux/mac
   venv\Scripts\activate     # windows
3. Install pytest for running tests:
   pip install pytest

## Run app
- Put `sample_data.json` in project root (or change DATA_FILE in cli.py)
- Run:
   python cli.py

## Tests
Run:
   pytest

## Notes
- Data persisted to `sample_data.json` by default.
- Analytics functions are in `analytics.py` using `map`, `filter`, and `reduce`.