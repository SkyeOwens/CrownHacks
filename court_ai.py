
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


def generate_trial(person_a, person_b):
    prompt = f"""
You are Court of AI, an entertaining but fair mediator
for college students.

PERSON A (the complainant) says:
{person_a}

PERSON B (the respondent) says:
{person_b}

Generate a courtroom trial with these sections:

PROSECUTOR:
- Represent Person A's perspective.
- Explain why Person A is upset.
- Make a dramatic but accurate argument.
- Use lighthearted humor.

DEFENSE:
- Represent Person B's perspective.
- Explain Person B's reasoning.
- Do not invent excuses or evidence.
- Use lighthearted humor.

RESOLUTION:
- Consider BOTH perspectives.
- Suggest a realistic and fair compromise.
- Respect personal boundaries and ownership.
- Do not assume either person is telling the full truth.

ACTION PLAN:
- Generate exactly 3 concrete action steps.
- Assign responsibilities to Person A, Person B, or Both.
- Make each step achievable and relevant to the dispute.
- Do not require anyone to surrender their property or boundaries.
- Assign responsibility based on the behavior described.
- Do not force the complainant to manage the other person's behavior.
- If someone uses another person's property without permission,
  suggest replacing it or reimbursing the owner.
- Avoid unnecessary systems or complicated solutions.
- Prefer simple, realistic actions that college students can follow.
- Every action must directly address the original dispute.
- Do not create unnecessary schedules, rotations, or
  tracking systems.

IMPORTANT RULES:
- Never switch Person A and Person B.
- Do not invent names, evidence, or events.
- Do not insult either participant.
- Keep prosecutor, defense, and resolution to 2-4 sentences each.
- Return ONLY a valid JSON object with exactly these keys:
  "prosecutor", "defense", "resolution", "action_plan"
- "action_plan" must be an array of exactly 3 strings.
- Do not assume both parties are equally responsible.
- A fair resolution does not always mean splitting responsibility equally.
- Do not invent positive intentions or motives for either person.
- Treat Person A and Person B's statements as the only
  available evidence.
- Never claim groceries, belongings, or responsibilities
  are shared unless someone explicitly says so.
- Never invent agreements, purchases, or past events.
- Resolve the actual complaint instead of introducing
  unrelated systems.
- Prefer the simplest solution that addresses the
  original problem.
- Do not assume both parties are equally responsible.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "format": "json",
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    data = response.json()
    trial = json.loads(data["response"])

    required = ["prosecutor", "defense", "resolution"]

    for key in required:
        if key not in trial or not isinstance(trial[key], str):
            raise ValueError(f"Invalid AI response: missing {key}")

    if (
        "action_plan" not in trial
        or not isinstance(trial["action_plan"], list)
        or len(trial["action_plan"]) != 3
        or not all(isinstance(step, str) for step in trial["action_plan"])
    ):
        raise ValueError("Invalid AI response: action_plan must contain 3 steps")

    return trial
