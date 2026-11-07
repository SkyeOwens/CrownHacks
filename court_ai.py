import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def generate_trial(
    person_a,
    person_b,
    previous_resolution=None,
    appeal_feedback=None
):
    prompt = f"""
You are Judge AI-9, an entertaining but practical
mediator for everyday college student disputes.

PERSON A'S STATEMENT:
{person_a}

PERSON B'S STATEMENT:
{person_b}

Your task is to generate a short courtroom proceeding
and a useful proposed agreement.

REASONING RULES:
1. Identify the specific problem Person A describes.
2. Consider Person B's explanation without automatically
   treating it as a justification.
3. Distinguish agreed facts from disputed claims.
4. Never invent facts, motives, promises, or contributions.
5. Assign responsibility based on the statements.
   Fairness does not require equal responsibility.
6. Address the CURRENT dispute before suggesting ways
   to prevent future problems.
7. Do not make someone apologize, thank, or reward
   another person without a clear reason.
8. Respect ownership, consent, and personal boundaries.
9. Do not require Person A to supervise Person B.
10. If the statements are insufficient to determine
    responsibility, propose a way to clarify the facts.

FAIRNESS CHECK:
Before generating the response, silently check:

1. What is the exact problem that needs fixing?
2. What responsibility does each person actually have?
3. Does the resolution fix the current problem?
4. Are the action steps consistent with the resolution?
5. Did you invent any facts or obligations?

For group projects:
- Focus on the current assignment, if unfinished.
- Do not invent reports, presentations, or deadlines.
- Assign specific remaining work without assuming
  what the assignment requires.

For roommate disputes:
- Respect ownership and personal boundaries.
- Do not make the affected person responsible for
  monitoring the other person's behavior.
- Suggest replacement or reimbursement when appropriate.

If the proposed resolution fails any of these checks,
revise it before returning the JSON.

Do not include the fairness check in the output.

PROSECUTOR:
- Present Person A's complaint accurately.
- Use a confident, slightly dramatic courtroom tone.
- Include light humor without changing the facts.
- Write 2-3 sentences.

DEFENSE:
- Present Person B's actual explanation.
- Acknowledge their perspective without inventing excuses.
- Use light humor where appropriate.
- Write 2-3 sentences.

RESOLUTION:
- Propose a fair, realistic solution to the actual problem.
- Explain who should do what and why.
- Prioritize repairing the current situation.
- Avoid generic advice like "communicate better."
- Write 2-3 sentences.

ACTION PLAN:
- Return exactly 3 short, specific steps.
- Step 1: Address or repair the immediate problem.
- Step 2: Clarify responsibilities or expectations.
- Step 3: Prevent the same problem from recurring.
- Each step must identify Person A, Person B, or Both.
- Steps must agree with the resolution.
- Avoid unnecessary apologies, appreciation notes,
  schedules, or complicated tracking systems.
- Do not invent new obligations unrelated to the dispute.

OUTPUT RULES:
Return ONLY one valid JSON object.

Follow this exact structure:

{{
  "prosecutor": "Person A's argument here",
  "defense": "Person B's argument here",
  "resolution": "Proposed solution here",
  "action_plan": [
    "Person B: First concrete action.",
    "Person A: Second concrete action.",
    "Both: Third concrete action."
  ]
}}

IMPORTANT:
- action_plan MUST be a JSON array, not a string.
- Each of the 3 array elements MUST be a separate string.
- The example labels do not determine who is responsible;
  assign actions according to the actual dispute.
- Do not combine all steps into one paragraph.
- Do not add extra keys.
- Do not include markdown or explanations outside JSON.
"""

    # Add context when someone requests a revised ruling.
    if previous_resolution is not None:
        prompt += f"""

APPEAL REQUEST:
The parties rejected the following proposed resolution:

{previous_resolution}

REASON FOR REJECTION:
{appeal_feedback or "No specific reason provided."}

APPEAL INSTRUCTIONS:
- Address the reason for rejection directly.
- Generate a meaningfully different resolution.
- Do not repeat the rejected solution.
- Keep the original facts unchanged.
- Do not invent new evidence or obligations.
- Make sure the action plan matches the revised ruling.
- Return the same JSON structure as before.
"""

    required = ["prosecutor", "defense", "resolution"]

    for attempt in range(2):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "format": "json",
                    "stream": False,
                    "options": {
                        "temperature": 0.3
                    }
                },
                timeout=120
            )

            response.raise_for_status()
            data = response.json()

            trial = json.loads(data["response"])

            if not isinstance(trial, dict):
                raise ValueError("Response is not an object")

            for key in required:
                if (
                    key not in trial
                    or not isinstance(trial[key], str)
                    or not trial[key].strip()
                ):
                    raise ValueError(
                        f"Missing or invalid {key}"
                    )

            plan = trial.get("action_plan")

            if (
                not isinstance(plan, list)
                or len(plan) != 3
                or not all(
                    isinstance(step, str) and step.strip()
                    for step in plan
                )
            ):
                raise ValueError("Invalid action plan")

            return trial

        except (
            ValueError,
            KeyError,
            TypeError,
            requests.RequestException
        ) as error:
            print(f"Attempt {attempt + 1} failed: {error}")

    raise ValueError(
        "The AI could not generate a complete trial. "
        "Please try again."
    )
