import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:7b"


def generate_trial(person_a, person_b, previous_resolution=None, appeal_feedback=None):
    prompt = f"""
You are Judge AI-9, an entertaining but practical mediator for everyday college student disputes.

PERSON A'S STATEMENT:
{person_a}

PERSON B'S STATEMENT:
{person_b}

Your task is to generate a short courtroom proceeding and a useful proposed agreement.

REASONING RULES:
1. Identify the exact current problem, its cause if supported, and the outcome each person needs.
2. Consider Person B's explanation without automatically treating it as a justification.
3. Distinguish agreed facts from disputed claims. Never present allegations as proven facts.
4. Never invent facts, motives, promises, resources, medical details, or contributions.
5. Assign responsibility based on the statements. Fairness does not require equal responsibility.
6. Repair any existing loss or harm BEFORE proposing prevention. If an item was consumed,
   damaged, or lost, consider replacement or reasonable reimbursement rather than return.
7. Do not make someone apologize, thank, or reward another person without a clear reason.
8. Respect ownership, consent, health needs, and personal boundaries.
9. Do not make the affected person supervise or manage the other person's behavior.
10. If the facts are insufficient to determine responsibility, suggest a reasonable way to clarify them.

SOLUTION QUALITY CHECK (perform silently before responding):
- State the problem in one precise sentence to yourself.
- For each proposed action, ask: Does this directly reduce the problem, or could it worsen it?
- Reject actions that merely move the disturbance to a different time, increase the disturbance,
  transfer responsibility to the affected person, or introduce an unrelated burden.
- Check feasibility: do not assume someone owns a device, can buy equipment, can change a
  medical schedule, or has access to resources not mentioned. Optional tools can be suggested
  conditionally, not mandated as if already available.
- When two legitimate needs conflict, preserve both where possible and choose the least
  disruptive realistic option. Do not recommend altering medication timing or dosage.
- Ensure each action has a clear owner and a reason tied to the dispute.
- If no guaranteed solution follows from the statements, acknowledge uncertainty and offer
  practical options or a small mutually agreed test rather than inventing certainty.
- Verify the three action steps match the resolution and do not contradict one another.
- Do not mistake preventing a future recurrence for fixing a past loss.
- Keep Person A as the complainant/prosecution and Person B as the respondent/defense.
  Do not invent explanations that either person did not give.
If any check fails, silently revise the proposal before producing JSON.

For group projects:
- Focus on the current assignment, if unfinished.
- Do not invent reports, presentations, or deadlines.
- Assign specific remaining work without assuming what the assignment requires.

For roommate disputes:
- Respect sleep, ownership, and personal boundaries.
- Do not make the affected person responsible for monitoring the other's behavior.
- If an alarm is waking someone else, do not propose an earlier or louder audible alarm as a
  fix unless the facts specifically establish that it would reduce the disturbance.
- Consider a quieter or private alert as an OPTIONAL option if practical, without assuming
  the person already owns the equipment or can afford it.
- Suggest replacement or reimbursement when appropriate.

PROSECUTOR:
- Present Person A's complaint accurately in 2-3 sentences.
- Use a confident, slightly dramatic courtroom tone with light humor that changes no facts.

DEFENSE:
- Present Person B's actual explanation in 2-3 sentences.
- Acknowledge their perspective without inventing excuses; light humor is fine.

RESOLUTION:
- Propose a fair, realistic solution to the actual problem in 2-3 sentences.
- If someone has already lost something, explain how that loss can be repaired.
  Only propose returning an item if the available facts indicate it still exists.
- Explain who should do what and why, prioritizing repair of the current situation.
- Avoid generic advice such as 'communicate better.'

ACTION PLAN:
- Return exactly 3 short, specific steps.
- Step 1: Address or repair the immediate problem.
- Step 2: Clarify responsibilities or expectations.
- Step 3: Prevent the same problem from recurring.
- Each step must identify Person A, Person B, or Both.
- Labels reflect actual responsibility; do not force one step onto each party.
- Avoid unnecessary apologies, schedules, tracking systems, and unrelated obligations.

OUTPUT RULES:
Return ONLY one valid JSON object in exactly this structure:
{{
  "prosecutor": "Person A's argument here",
  "defense": "Person B's argument here",
  "resolution": "Proposed solution here",
  "action_plan": [
    "Person B: First concrete action.",
    "Person B: Second concrete action.",
    "Both: Third concrete action."
  ]
}}
The labels in this example are illustrative, not required assignments.
The action_plan must be an array of exactly three separate strings.
Do not add keys, markdown, or commentary outside the JSON.
"""

    if previous_resolution is not None:
        prompt += f"""

APPEAL REQUEST:
The parties rejected this proposed resolution:
{previous_resolution}

REASON FOR REJECTION:
{appeal_feedback or 'No specific reason provided.'}

APPEAL INSTRUCTIONS:
- Identify precisely what the objection says was wrong with the previous proposal.
- Treat the objection as feedback to evaluate, not as automatically proven fact.
- An objection may introduce a new relevant fact (for example, that food was already eaten).
  Incorporate plausible new facts conditionally, without presenting disputed claims as verified.
- If a proposed repair is now impossible, replace it with a feasible repair.
  Do not respond only with future-prevention steps.
- Do not repeat or cosmetically reword the rejected solution.
- Specifically test the new solution against the objection: if it repeats the harm,
  increases the original problem, or shifts responsibility unfairly, revise it.
- Preserve the original facts and legitimate needs of both parties.
- Do not invent evidence, purchases, resources, or obligations.
- Make the revised action plan consistent with the revised ruling.
- Return the same JSON structure.
"""

    def ask_ollama(message):
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": message,
                "format": "json",
                "stream": False,
                "options": {"temperature": 0.2},
            },
            timeout=120,
        )
        response.raise_for_status()
        return json.loads(response.json()["response"])

    def validate_trial(trial):
        if not isinstance(trial, dict):
            raise ValueError("Response is not a JSON object")
        for key in ("prosecutor", "defense", "resolution"):
            if not isinstance(trial.get(key), str) or not trial[key].strip():
                raise ValueError(f"Missing or invalid {key}")
        plan = trial.get("action_plan")
        if (not isinstance(plan, list) or len(plan) != 3
                or not all(isinstance(step, str) and step.strip() for step in plan)):
            raise ValueError("Invalid action plan")
        return trial

    def critique(trial):
        # Separate model call: assess the proposal against the ORIGINAL statements.
        review_prompt = f"""
You are an independent quality reviewer, NOT the judge. Review ALL FOUR fields
(prosecutor, defense, resolution, action_plan) critically. Do not assume a
proposal is fair just because it sounds polite. Judge only against the
statements and appeal feedback provided; do not invent missing facts.

PERSON A'S ORIGINAL STATEMENT:
{person_a}

PERSON B'S ORIGINAL STATEMENT:
{person_b}

PREVIOUS REJECTED RESOLUTION:
{previous_resolution if previous_resolution is not None else 'None'}

APPEAL FEEDBACK:
{appeal_feedback or 'None'}

CANDIDATE RULING (JSON):
{json.dumps(trial, ensure_ascii=False)}

FAIL the candidate if ANY of these are true:
- It misidentifies which person is affected or responsible.
- The prosecutor misrepresents Person A or the defense misrepresents Person B,
  including reversing a complaint or inventing an explanation.
- It presents unsupported claims about past events as established facts.
- Do not reject a reasonable proposed action merely because neither person
  mentioned it, such as replacing eaten food or labeling belongings.
- Proposed actions are recommendations, not claims about what already happened.
- Reject actions that are impractical, unrelated, unfairly assigned, or assume
  resources the parties have not established are available.
- It shifts the burden of fixing the problem onto the affected person without reason.
- Its steps do not actually address the source of the original complaint.
- It fails to repair an existing loss or harm when a feasible repair is available.
- It focuses on labeling, rules, or communication while ignoring an existing
  loss such as consumed food, damaged property, or unfinished assigned work.
- It proposes returning an item that the appeal says is already consumed or gone,
  rather than considering replacement or reimbursement.
- A proposed change could reproduce or worsen the original harm.
- On appeal, it repeats the rejected idea or fails to address a reasonable objection.
- On appeal, it fails to adapt to plausible new information in the feedback.
  Treat new claims as claims, not automatically verified facts.
- Its action plan contradicts the resolution or imposes unrelated obligations.
- It assumes someone can change a medical schedule or owns special equipment.

In particular, if an audible alarm wakes a roommate, moving it EARLIER does
not solve the noise problem. Do not assign the disturbed roommate a wake-up duty
unless their own statement establishes one. A quieter/private alert can be
suggested conditionally without assuming equipment is available.

The parties' statements and feedback may themselves be disputed; do not
assume either is necessarily true. Evaluate what follows from the evidence.

Before deciding, explicitly evaluate these three tests internally:
REPAIR: Does the plan address the existing harm, not just future prevention?
RESPONSIBILITY: Are obligations assigned to the appropriate party?
APPEAL: If present, is the specific objection or new information addressed?
A candidate must pass ALL THREE. When a test fails, return passes=false and
name the failing test with a concrete correction in criticism.
For example, if food was eaten, labeling trays alone cannot replace that food.
A reasonable repair could be replacement or reimbursement, subject to facts.

Return ONLY JSON with exactly these fields:
{{"passes": false, "criticism": "Specific, actionable reason it fails."}}
OR
{{"passes": true, "criticism": ""}}
"""
        review = ask_ollama(review_prompt)
        if not isinstance(review, dict) or type(review.get("passes")) is not bool:
            raise ValueError("Invalid reviewer response")
        if not review["passes"] and (not isinstance(review.get("criticism"), str)
                                     or not review["criticism"].strip()):
            raise ValueError("Reviewer did not explain rejection")
        return review

    # One initial candidate, up to two targeted revisions. Fail closed rather
    # than displaying a ruling the reviewer still finds harmful or incoherent.
    last_error = None
    current_prompt = prompt
    for attempt in range(1):
        try:
            trial = validate_trial(ask_ollama(current_prompt))
            return trial
            if review["passes"]:
                return trial

            criticism = review.get("criticism", "The proposed ruling did not solve the dispute.")
            print(f"Ruling rejected by reviewer (round {attempt + 1}): {criticism}")
            last_error = criticism
            current_prompt = prompt + f"""

THE PREVIOUS CANDIDATE FAILED INDEPENDENT REVIEW.
Candidate: {json.dumps(trial, ensure_ascii=False)}
Specific reviewer criticism: {criticism}

Generate a materially corrected ruling that fixes the criticism. Do not
repeat the flawed action, shift the burden to the affected party, or invent
new facts. Return only the original trial JSON schema.
"""
        except (ValueError, KeyError, TypeError, requests.RequestException) as error:
            last_error = str(error)
            print(f"Generation/review attempt {attempt + 1} failed: {error}")

    raise ValueError(
        "The court could not verify a fair resolution after several attempts. "
        "Please retry or clarify the statements. "
        f"Last issue: {last_error}"
    )
