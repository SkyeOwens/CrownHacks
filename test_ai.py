
from court_ai import generate_trial

cases = [
    (
        "Roommate Groceries",
        "My roommate keeps eating my groceries without asking.",
        "I thought the groceries were for everyone."
    ),
    (
        "Dirty Dishes",
        "My roommate leaves dirty dishes in the sink for days.",
        "I've been overwhelmed with exams and haven't had time."
    ),
    (
        "Group Project",
        "My teammate hasn't completed their assigned work.",
        "I've been struggling to understand the assignment."
    )
]

for title, person_a, person_b in cases:
    print("\n" + "=" * 50)
    print("CASE:", title)
    print("=" * 50)

    try:
        trial = generate_trial(person_a, person_b)

        print("\nPROSECUTOR:")
        print(trial["prosecutor"])

        print("\nDEFENSE:")
        print(trial["defense"])

        print("\nRESOLUTION:")
        print(trial["resolution"])

        print("\nACTION PLAN:")
        for step in trial["action_plan"]:
            print("-", step)

    except Exception as error:
        print("ERROR:", error)
