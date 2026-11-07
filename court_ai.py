
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

Generate three courtroom responses:

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
- Include specific actions both people can take.

IMPORTANT RULES:
- Never switch Person A and Person B.
- Do not invent names, evidence, or events.
- Do not insult either participant.
- Keep each response to 2-4 sentences.
- Do not assume either person is telling the full truth.
- Return ONLY valid JSON with exactly these keys:
  "prosecutor", "defense", "resolution"
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

    return trial
