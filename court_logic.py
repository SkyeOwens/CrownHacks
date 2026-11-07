"""Shared settings, achievements and unlockables for Court of AI."""
import json
import os
import re

MAX_ROUNDS = 3

# Progress is saved next to this file so achievements survive closing the app.
PROGRESS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progress.json")

# ---------------------------------------------------------------------
#  ACHIEVEMENTS
# ---------------------------------------------------------------------
ACHIEVEMENTS = {
    "first_trial": {"icon": "⚖️", "name": "Order in the Court", "desc": "Finish your first trial."},
    "settled_r1": {"icon": "🤝", "name": "Settled in Round 1", "desc": "Both parties accept the very first resolution."},
    "round3": {"icon": "🥊", "name": "Made It to Round 3", "desc": "Take a case all the way to round 3."},
    "snack": {"icon": "🍟", "name": "Snack Crimes Specialist", "desc": "Settle a case about food."},
    "roommate": {"icon": "🛏️", "name": "Roommate Diplomat", "desc": "Settle a case between roommates."},
    "hung": {"icon": "🧱", "name": "Hung Jury", "desc": "Run out of resolution attempts."},
    "peacemaker": {"icon": "🕊️", "name": "Peacemaker", "desc": "Settle 5 cases."},
    "regular": {"icon": "📚", "name": "Court Regular", "desc": "Finish 10 trials."},
}

FOOD_WORDS = {
    "fries", "food", "snack", "snacks", "groceries", "grocery", "pizza", "chips", "eat", "ate",
    "eating", "lunch", "dinner", "breakfast", "leftover", "leftovers", "fridge", "cookie", "cookies",
    "candy", "drink", "soda", "coffee", "ramen", "cereal", "milk", "sandwich",
}

# ---------------------------------------------------------------------
#  UNLOCKABLES  ("needs" = number of settled cases required)
# ---------------------------------------------------------------------
THEMES = {
    "classic": {"name": "Grand Courtroom", "needs": 0},
    "dorm": {"name": "Dorm Room", "needs": 1},
    "dining": {"name": "Dining Hall", "needs": 3},
    "library": {"name": "Library", "needs": 5},
}

OUTFITS = {
    "classic": {"name": "Classic", "needs": 0},
    "formal": {"name": "Formal Night", "needs": 2},
    "party": {"name": "Party Mode", "needs": 4},
}


# ---------------------------------------------------------------------
#  SAVE FILE
# ---------------------------------------------------------------------
def default_progress():
    return {"trials": 0, "settled": 0, "achievements": [], "theme": "classic", "outfit": "classic"}


def load_progress():
    progress = default_progress()
    try:
        with open(PROGRESS_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)
        if isinstance(saved, dict):
            progress.update(saved)
    except (OSError, ValueError):
        pass  # no save file yet, or it's broken: start fresh
    return progress


def save_progress(progress):
    try:
        with open(PROGRESS_FILE, "w", encoding="utf-8") as file:
            json.dump(progress, file, indent=2)
    except OSError:
        pass


def unlocked(options, progress):
    """Keys from THEMES or OUTFITS that this save file has earned."""
    return [key for key, item in options.items() if progress["settled"] >= item["needs"]]


def record_verdict(progress, case, round_number, settled, max_rounds=MAX_ROUNDS):
    """Update the save file after a verdict.
    Returns (new achievement ids, names of newly unlocked courtrooms/outfits)."""
    themes_before = set(unlocked(THEMES, progress))
    outfits_before = set(unlocked(OUTFITS, progress))

    progress["trials"] += 1
    if settled:
        progress["settled"] += 1

    text = f'{case["person_a"]} {case["person_b"]}'.lower()
    words = set(re.findall(r"[a-z']+", text))
    earned = {
        "first_trial": True,
        "settled_r1": settled and round_number == 1,
        "round3": round_number >= 3,
        "snack": settled and bool(words & FOOD_WORDS),
        "roommate": settled and ("roommate" in text or "roomate" in text),
        "hung": (not settled) and round_number >= max_rounds,
        "peacemaker": progress["settled"] >= 5,
        "regular": progress["trials"] >= 10,
    }
    new_achievements = [key for key, ok in earned.items() if ok and key not in progress["achievements"]]
    progress["achievements"].extend(new_achievements)

    new_unlocks = (
        [THEMES[key]["name"] + " courtroom" for key in unlocked(THEMES, progress) if key not in themes_before]
        + [OUTFITS[key]["name"] + " outfits" for key in unlocked(OUTFITS, progress) if key not in outfits_before]
    )
    return new_achievements, new_unlocks
