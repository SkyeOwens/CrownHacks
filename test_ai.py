
from court_ai import generate_trial

result = generate_trial(
    "My roommate keeps eating my groceries without asking.",
    "I thought the groceries were for everyone."
)

print("\nPROSECUTOR:")
print(result["prosecutor"])

print("\nDEFENSE:")
print(result["defense"])

print("\nRESOLUTION:")
print(result["resolution"])

print("\nACTION PLAN:")
for step in result["action_plan"]:
    print("-", step)
