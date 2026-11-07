import streamlit as st

st.set_page_config(
    page_title="Court of AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Original courtroom visual-novel styling (inspired by dramatic courtroom games) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Libre+Baskerville:wght@700&family=Rajdhani:wght@500;600;700&display=swap');

:root {
  --ink: #eaf1f8;
  --muted: #aab8c8;
  --navy: #101b2c;
  --panel: #19283d;
  --panel2: #223650;
  --red: #b83b43;
  --gold: #e4bd68;
}
.stApp {
  background:
    radial-gradient(ellipse at 50% -15%, rgba(75,104,139,.38), transparent 55%),
    linear-gradient(135deg, #0a1220 0%, #15243a 55%, #0b1422 100%);
  color: var(--ink);
}
.block-container {max-width: 1120px; padding-top: 1.5rem; padding-bottom: 3rem;}
h1, h2, h3 {font-family: 'Libre Baskerville', Georgia, serif !important; color: #f5e7c4 !important;}
p, label, div, span {font-family: 'Rajdhani', sans-serif;}
.hero {
  border: 1px solid rgba(228,189,104,.55);
  background: linear-gradient(115deg, rgba(24,39,60,.98), rgba(42,35,43,.96));
  padding: 1.5rem 1.8rem; border-radius: 8px; text-align:center;
  box-shadow: 0 12px 35px rgba(0,0,0,.28);
  margin-bottom: 1.2rem;
}
.hero-kicker {font: 500 .78rem 'DM Mono', monospace; color:var(--gold); letter-spacing:.22em;}
.hero-title {font:700 clamp(2rem,5vw,3.5rem) 'Libre Baskerville',serif; color:#fff1d0; margin:.4rem 0;}
.hero-sub {color:#b9c7d7; font-size:1.08rem; letter-spacing:.08em;}
.case-strip {
  background:#0b1422; border:1px solid #52647a; border-left:5px solid var(--gold);
  padding:.7rem 1rem; border-radius:5px; margin:.8rem 0 1rem;
  font:500 .85rem 'DM Mono',monospace; color:#e9d7ac;
}
.panel {
  background:linear-gradient(145deg, rgba(32,51,75,.98), rgba(19,32,49,.98));
  border:1px solid #52647a; border-radius:8px; padding:1.15rem 1.3rem;
  box-shadow:0 8px 24px rgba(0,0,0,.2); margin:.5rem 0 1rem;
}
.panel-label {font:500 .75rem 'DM Mono',monospace; color:var(--gold); letter-spacing:.16em; text-transform:uppercase; margin-bottom:.55rem;}
.dialogue {
  background:linear-gradient(120deg,#101a29,#1b2b41);
  border:1px solid #71839a; border-top:4px solid var(--red);
  border-radius:7px; padding:1.25rem 1.4rem; margin:.5rem 0 1rem;
  box-shadow:0 10px 25px rgba(0,0,0,.28);
}
.dialogue-name {font:700 1.05rem 'DM Mono',monospace; color:#f1c96f; margin-bottom:.55rem;}
.dialogue-text {font-size:1.16rem; line-height:1.55; color:#f0f4f8;}
.stButton>button {
  background:linear-gradient(180deg,#c84c50,#8f2835) !important;
  color:white !important; border:1px solid #ef9a83 !important;
  border-radius:5px !important; font:700 1rem 'Rajdhani',sans-serif !important;
  letter-spacing:.08em !important; text-transform:uppercase !important;
  box-shadow:0 4px 0 #591c28 !important; min-height:2.7rem;
}
.stButton>button:hover {filter:brightness(1.14); border-color:#ffe0a0 !important;}
.stTextInput input, .stTextArea textarea {
  background:#0d1929 !important; color:#f4f6f8 !important;
  border:1px solid #71839a !important; border-radius:5px !important;
}
.stCheckbox label {color:#eaf1f8 !important;}
.verdict {
  text-align:center; padding:1rem; border:2px solid var(--gold); border-radius:7px;
  background:linear-gradient(120deg,#17263a,#332d2b); margin:1rem 0;
}
.verdict-word {font:700 clamp(1.8rem,4vw,3rem) 'Libre Baskerville',serif; color:#f4d17d;}
.small-note {color:#b7c4d2; font: .8rem 'DM Mono',monospace;}
hr {border-color:#52647a !important;}
</style>
""", unsafe_allow_html=True)

# Detect whether the live backend is available.
try:
    from court_ai import generate_trial
    BACKEND_AVAILABLE = True
except ImportError:
    generate_trial = None
    BACKEND_AVAILABLE = False

from court_logic import MAX_ROUNDS

SAMPLE_TITLE = "The Case of the Missing Dining Hall Fries"
SAMPLE_A = "I bought fries and left them on the table for a minute. When I came back, they were gone."
SAMPLE_B = "I thought they were leftovers from the group order. I should have asked first."

def demo_trial(person_a, person_b):
    return {
        "prosecutor": f"Person A says: {person_a} The complaint is that their side of the story was not respected.",
        "defense": f"Person B says: {person_b} That explanation matters, but asking first would have avoided the dispute.",
        "resolution": "Person A deserves to have their belongings respected. Person B should acknowledge the mistake and make it right without turning a small disagreement into a bigger conflict.",
        "action_plan": [
            "Person B: Apologize directly to Person A for taking the fries without checking.",
            "Person B: Replace the fries or reimburse Person A for their cost.",
            "Both: Ask before taking food or belongings that may belong to someone else."
        ]
    }

def init_state():
    defaults = {
        "case": None, "stage": "SUBMIT", "trial": None, "round": 1,
        "choices": {"a": None, "b": None},
        "in_title": "", "in_claim_a": "", "in_claim_b": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_trial():
    st.session_state.case = None
    st.session_state.stage = "SUBMIT"
    st.session_state.trial = None
    st.session_state.round = 1
    st.session_state.choices = {"a": None, "b": None}
    st.session_state.in_title = ""
    st.session_state.in_claim_a = ""
    st.session_state.in_claim_b = ""

def make_trial(a, b, demo):
    if demo:
        return demo_trial(a, b)
    if not BACKEND_AVAILABLE:
        raise RuntimeError("The court_ai.py backend could not be imported. Add court_ai.py to this folder or turn on Demo Mode.")
    return generate_trial(a, b)

def validate_trial(trial):
    for key in ("prosecutor", "defense", "resolution"):
        if key not in trial or not isinstance(trial[key], str):
            raise ValueError(f"AI backend returned an invalid response: missing {key}.")
    plan = trial.get("action_plan", [])
    if not isinstance(plan, list) or not all(isinstance(item, str) for item in plan):
        raise ValueError("AI backend returned an invalid action plan.")
    return trial

def start_trial():
    title = st.session_state.in_title.strip()
    a = st.session_state.in_claim_a.strip()
    b = st.session_state.in_claim_b.strip()
    errors = 0
    if not a:
        st.error("Person A's statement is required.")
        errors += 1
    if not b:
        st.error("Person B's statement is required.")
        errors += 1
    if errors:
        return
    try:
        trial = validate_trial(make_trial(a, b, st.session_state.use_demo))
    except Exception as exc:
        message = str(exc)
        if "11434" in message or "connection" in message.lower() or "refused" in message.lower():
            st.error("The court cannot reach Ollama. Make sure Ollama is running and the model is installed.")
        else:
            st.error(f"Could not start the trial: {message}")
        return
    st.session_state.case = {
        "title": title or "Untitled Case",
        "person_a": a,
        "person_b": b,
    }
    st.session_state.trial = trial
    st.session_state.stage = "PROSECUTION"
    st.session_state.round = 1
    st.session_state.choices = {"a": None, "b": None}

def advance():
    order = ["PROSECUTION", "DEFENSE", "RESOLUTION", "AGREEMENT"]
    current = order.index(st.session_state.stage)
    st.session_state.stage = order[min(current + 1, len(order) - 1)]

def choose(side, value):
    st.session_state.choices[side] = value

def retry_resolution():
    st.session_state.round += 1
    a, b = st.session_state.case["person_a"], st.session_state.case["person_b"]
    try:
        updated = validate_trial(make_trial(a, b, st.session_state.use_demo))
        # Preserve the original opening arguments; ask for a fresh resolution.
        st.session_state.trial["resolution"] = updated["resolution"] + f" (Resolution round {st.session_state.round}.)"
        if updated.get("action_plan"):
            st.session_state.trial["action_plan"] = updated["action_plan"]
    except Exception as exc:
        st.error(f"The court could not prepare another resolution: {exc}")
        st.session_state.round -= 1
        return
    st.session_state.choices = {"a": None, "b": None}
    st.session_state.stage = "RESOLUTION"

    

init_state()

st.markdown("""
<div class="hero">
  <div class="hero-kicker">✦ THE PEOPLE'S COURT · EST. 2026 ✦</div>
  <div class="hero-title">⚖ COURT OF AI</div>
  <div class="hero-sub">OBJECTION! Your side of the story is now in session.</div>
</div>
""", unsafe_allow_html=True)

if st.session_state.case is None:
    st.markdown('<div class="case-strip">CASE FILE 001 · NEW MATTER · AWAITING STATEMENTS</div>', unsafe_allow_html=True)
    st.markdown('<div class="panel"><div class="panel-label">Before the court</div><h3>Every great trial starts with two sides.</h3><p>Present both statements. The court will hear the arguments, consider a compromise, and issue an action plan.</p></div>', unsafe_allow_html=True)
    st.text_input("Case title (optional)", key="in_title", placeholder="e.g. The Case of the Stolen Snacks")
    left, right = st.columns(2)
    with left:
        st.markdown("### 🟥 Person A · Complainant")
        st.text_area("What happened from Person A's perspective?", key="in_claim_a", height=160, placeholder="Explain what happened and why you're upset...")
    with right:
        st.markdown("### 🟦 Person B · Respondent")
        st.text_area("What happened from Person B's perspective?", key="in_claim_b", height=160, placeholder="Explain your side of the story...")
    st.checkbox("Use Demo Mode (no Ollama required)", key="use_demo", value=not BACKEND_AVAILABLE)
    c1, c2 = st.columns([1, 1])
    with c1:
        st.button("Load Sample Case", key="load_sample", use_container_width=True,
                  on_click=lambda: st.session_state.update({
                      "in_title": SAMPLE_TITLE, "in_claim_a": SAMPLE_A, "in_claim_b": SAMPLE_B
                  }))
    with c2:
        st.button("⚖ Start Trial", key="start", use_container_width=True, on_click=start_trial)
    st.markdown('<p class="small-note">COURT NOTICE: The AI mediator is not a real judge. Keep statements respectful and avoid sharing private information.</p>', unsafe_allow_html=True)

else:
    case = st.session_state.case
    st.markdown(f'<div class="case-strip">CASE FILE · {case["title"].upper()} · ROUND {st.session_state.round}</div>', unsafe_allow_html=True)
    with st.expander("📁 View submitted statements", expanded=False):
        a_col, b_col = st.columns(2)
        with a_col:
            st.markdown("**PERSON A**")
            st.write(case["person_a"])
        with b_col:
            st.markdown("**PERSON B**")
            st.write(case["person_b"])

    if st.session_state.stage == "PROSECUTION":
        st.markdown('<div class="panel-label">01 / Opening argument</div><h2>PROSECUTION!</h2>', unsafe_allow_html=True)
        st.markdown('<div class="dialogue"><div class="dialogue-name">🟥 COUNSEL FOR PERSON A</div><div class="dialogue-text">The complainant calls upon the court to hear the facts!</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dialogue"><div class="dialogue-name">PROSECUTOR</div><div class="dialogue-text">{st.session_state.trial["prosecutor"]}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="panel-label">DEFENSE</div>🔒 WAITING FOR THE COURT</div><div class="panel"><div class="panel-label">RESOLUTION</div>🔒 WAITING FOR THE COURT</div>', unsafe_allow_html=True)
        st.button("Proceed to the defense  →", key="next", on_click=advance)

    elif st.session_state.stage == "DEFENSE":
        st.markdown('<div class="panel-label">02 / The response</div><h2>THE DEFENSE</h2>', unsafe_allow_html=True)
        st.markdown('<div class="dialogue"><div class="dialogue-name">🟦 COUNSEL FOR PERSON B</div><div class="dialogue-text">The respondent is ready to present their side!</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="dialogue"><div class="dialogue-name">DEFENSE</div><div class="dialogue-text">{st.session_state.trial["defense"]}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="panel"><div class="panel-label">RESOLUTION</div>🔒 WAITING FOR THE COURT</div>', unsafe_allow_html=True)
        st.button("Proceed to deliberation  →", key="next", on_click=advance)

    elif st.session_state.stage == "RESOLUTION":
        st.markdown('<div class="panel-label">03 / The court considers both sides</div><h2>JUDICIAL DELIBERATION</h2>', unsafe_allow_html=True)
        st.markdown(f'<div class="dialogue"><div class="dialogue-name">THE COURT</div><div class="dialogue-text">{st.session_state.trial["resolution"]}</div></div>', unsafe_allow_html=True)
        plan = st.session_state.trial.get("action_plan", [])
        if plan:
            st.markdown('<div class="panel-label">📜 Court-ordered action plan</div>', unsafe_allow_html=True)
            for index, step in enumerate(plan, 1):
                st.markdown(f'<div class="panel"><span class="panel-label">ACTION {index:02d}</span><br>{step}</div>', unsafe_allow_html=True)
        st.button("Proceed to agreement  →", key="next", on_click=advance)


    elif st.session_state.stage == "AGREEMENT":
        st.markdown('<div class="panel-label">04 / Final decision</div><h2>DO THE PARTIES AGREE?</h2>', unsafe_allow_html=True)
        st.markdown('<div class="dialogue"><div class="dialogue-name">THE COURT</div><div class="dialogue-text">Both parties must choose whether they accept the proposed resolution. The verdict will be revealed once both have answered.</div></div>', unsafe_allow_html=True)
        a_col, b_col = st.columns(2)
        with a_col:
            st.markdown("### 🟥 Person A")
            st.write("Do you accept the resolution?")
            st.button("✓ Accept", key="accept_a", disabled=st.session_state.choices["a"] is not None, on_click=choose, args=("a", "accept"), use_container_width=True)
            st.button("✕ Decline", key="decline_a", disabled=st.session_state.choices["a"] is not None, on_click=choose, args=("a", "decline"), use_container_width=True)
            if st.session_state.choices["a"]:
                st.caption(f"Answer recorded: {st.session_state.choices['a'].upper()}")
        with b_col:
            st.markdown("### 🟦 Person B")
            st.write("Do you accept the resolution?")
            st.button("✓ Accept", key="accept_b", disabled=st.session_state.choices["b"] is not None, on_click=choose, args=("b", "accept"), use_container_width=True)
            st.button("✕ Decline", key="decline_b", disabled=st.session_state.choices["b"] is not None, on_click=choose, args=("b", "decline"), use_container_width=True)
            if st.session_state.choices["b"]:
                st.caption(f"Answer recorded: {st.session_state.choices['b'].upper()}")
        if all(st.session_state.choices.values()):
            st.button("⚖ Reveal Verdict", key="see_verdict", use_container_width=True,
                      on_click=lambda: st.session_state.update({"stage": "VERDICT"}))

    elif st.session_state.stage == "VERDICT":
        accepted = all(value == "accept" for value in st.session_state.choices.values())
        if accepted:
            st.markdown('<div class="verdict"><div class="verdict-word">CASE SETTLED</div><p>The parties have accepted the court’s resolution.</p></div>', unsafe_allow_html=True)
            st.markdown("### Final action plan")
            for index, step in enumerate(st.session_state.trial.get("action_plan", []), 1):
                st.markdown(f'<div class="panel"><span class="panel-label">ACTION {index:02d}</span><br>{step}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="verdict"><div class="verdict-word">NO DEAL</div><p>The proposed resolution was not accepted by both parties.</p></div>', unsafe_allow_html=True)
            if st.session_state.round < MAX_ROUNDS:
                st.write("The court may attempt another resolution.")
                st.button("Request another resolution", key="retry", on_click=retry_resolution)
            else:
                st.warning("The court has reached its maximum number of resolution attempts.")
        st.button("Start a new trial", key="reset_verdict", on_click=reset_trial)

    st.divider()
    if st.session_state.stage != "VERDICT":
        st.button("↺ Abandon case / New trial", key="reset_sidebar", on_click=reset_trial)
    st.markdown('<p class="small-note">COURT OF AI · A fictional mediation experience, not legal advice.</p>', unsafe_allow_html=True)

    
