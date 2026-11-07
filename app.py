import base64
import html

import streamlit as st

st.set_page_config(
    page_title="Court of AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =====================================================================
#  PIXEL COURTROOM STYLING
#  Blocky fonts, hard pixel borders, visual-novel dialogue boxes.
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
:root {
  --ink: #f4f1e8;
  --gold: #f2c14e;
  --red: #d8434b;
  --blue: #3f7fd8;
  --purple: #8a6ad8;
  --black: #05060c;
}
.stApp {
  background-color: #141026;
  background-image:
    linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
  background-size: 8px 8px;
  color: var(--ink);
}
.block-container {max-width: 980px; padding-top: 1.2rem; padding-bottom: 3rem;}
.stApp p, .stApp label, .stApp li, .stMarkdown {font-family: 'VT323', monospace; font-size: 1.3rem;}
h1, h2, h3, .px {font-family: 'Press Start 2P', monospace !important; color: var(--gold) !important; letter-spacing: .02em;}
h3 {font-size: .95rem !important; line-height: 1.6 !important;}
/* ---------- title card ---------- */
.hero {
  text-align: center; padding: 1.4rem 1rem 1.2rem; margin-bottom: 1.2rem;
  background: #231a3d; border: 4px solid var(--ink); outline: 4px solid var(--black);
  box-shadow: 8px 8px 0 var(--black);
}
.hero-kicker {font: .6rem 'Press Start 2P', monospace; color: var(--gold); letter-spacing: .18em;}
.hero-title {
  font: clamp(1.6rem, 5vw, 2.8rem) 'Press Start 2P', monospace; color: #fff;
  margin: .9rem 0 .7rem; text-shadow: 4px 4px 0 var(--red), 8px 8px 0 var(--black);
}
.hero-sub {font: 1.5rem 'VT323', monospace; color: #cfc6e8;}
/* ---------- case strip + stage tracker ---------- */
.case-strip {
  background: var(--black); border: 4px solid #4a4370; border-left: 12px solid var(--gold);
  padding: .65rem 1rem; margin: .4rem 0 .9rem;
  font: .62rem/1.7 'Press Start 2P', monospace; color: var(--gold);
}
.tracker {display: flex; gap: 6px; margin: 0 0 1rem; flex-wrap: wrap;}
.pip {
  flex: 1; min-width: 110px; text-align: center; padding: .5rem .3rem;
  font: .5rem 'Press Start 2P', monospace; color: #6f6896;
  background: #1d1733; border: 3px solid #3a335c;
}
.pip.done {color: #b9b2d8; border-color: #5b5390;}
.pip.now {color: var(--black); background: var(--gold); border-color: var(--ink); box-shadow: 3px 3px 0 var(--black);}
/* ---------- wood-paneled courtroom backdrop ---------- */
.courtroom {
  position: relative; padding: 1.4rem 1.2rem 1.6rem; margin: .3rem 0 1.2rem;
  border: 4px solid var(--ink); outline: 4px solid var(--black); box-shadow: 8px 8px 0 var(--black);
  background-color: #5e3b20;
  background-image:
    linear-gradient(180deg, rgba(20,12,6,.0) 0 62%, rgba(20,12,6,.55) 62% 100%),
    repeating-linear-gradient(90deg, #6e4526 0 56px, #5a371c 56px 60px);
}
.map-title {
  display: inline-block; margin: 0 0 1.1rem; padding: .55rem .8rem;
  font: .62rem 'Press Start 2P', monospace; color: var(--black); background: var(--gold);
  border: 4px solid var(--black); box-shadow: 4px 4px 0 var(--black);
}
.map-row {display: flex; align-items: center; justify-content: center; gap: .6rem; flex-wrap: wrap;}
/* ---------- character cards ---------- */
.card {
  --frame: var(--blue); --frame-dark: #1d3f78;
  width: 230px; flex: none; background: var(--frame-dark);
  border: 6px solid var(--frame); outline: 4px solid var(--black); box-shadow: 7px 7px 0 var(--black);
  animation: hop .4s steps(4) both;
}
.card.pros  {--frame: #b05bd6; --frame-dark: #4a2160;}
.card.def   {--frame: #4b8fe8; --frame-dark: #1c3b6e;}
.card.judge {--frame: #f2a33a; --frame-dark: #6b3d10;}
.card.big {width: 250px;}
.card-portrait {
  display: flex; justify-content: center; align-items: flex-end; height: 200px;
  background: linear-gradient(180deg, #e9eef8 0 70%, #c6d2e6 70% 100%);
  border-bottom: 6px solid var(--frame); overflow: hidden;
}
.card-portrait img {image-rendering: pixelated; display: block;}
.card-name {
  padding: .6rem .55rem .35rem; font: .58rem/1.6 'Press Start 2P', monospace; color: #fff;
  text-shadow: 2px 2px 0 var(--black);
}
.card-name span {color: var(--gold);}
.card-bio {padding: 0 .65rem .75rem; font: 1.15rem/1.15 'VT323', monospace; color: #e6e2f3;}
@keyframes hop {from {transform: translateY(18px); opacity: 0;} to {transform: translateY(0); opacity: 1;}}
/* ---------- relationship links ---------- */
.link {display: flex; flex-direction: column; align-items: center; gap: .45rem; min-width: 120px; padding: 0 .3rem;}
.link-label {
  padding: .4rem .5rem; text-align: center; font: .45rem/1.7 'Press Start 2P', monospace;
  color: var(--black); background: #f4f1e8; border: 3px solid var(--black);
}
.link-line {position: relative; width: 110px; height: 8px; background: var(--gold); border: 2px solid var(--black);}
.link-line::before, .link-line::after {
  content: ""; position: absolute; top: 50%; transform: translateY(-50%);
  border: 10px solid transparent;
}
.link-line::before {left: -20px; border-right-color: var(--gold);}
.link-line::after {right: -20px; border-left-color: var(--gold);}
.link.down {margin: 1rem 0 .8rem;}
.link.down .link-line {width: 8px; height: 40px;}
.link.down .link-line::before {display: none;}
.link.down .link-line::after {left: 50%; right: auto; top: auto; bottom: -20px; transform: translateX(-50%); border-left-color: transparent; border-top-color: var(--gold);}
/* ---------- trial stage: card + dialogue side by side ---------- */
.stage-row {display: flex; gap: 1.4rem; align-items: flex-end; flex-wrap: wrap;}
.stage-row .vn-col {flex: 1; min-width: 260px;}
.stage-row .vn-box {margin-bottom: 0;}
.duo {display: flex; justify-content: space-around; gap: 1rem; flex-wrap: wrap;}
/* ---------- visual-novel dialogue box ---------- */
.vn-box {
  position: relative; margin: 1.9rem 0 1.1rem; padding: 1.7rem 1.4rem 1.6rem;
  background: rgba(10, 12, 32, .96);
  border: 4px solid var(--ink); outline: 4px solid var(--black);
  box-shadow: 8px 8px 0 var(--black);
}
.vn-name {
  position: absolute; top: -1.35rem; left: 1rem; padding: .5rem .8rem;
  font: .62rem 'Press Start 2P', monospace; color: #fff; background: var(--tag, var(--purple));
  border: 4px solid var(--ink); outline: 4px solid var(--black);
}
.vn-text {font: 1.6rem/1.3 'VT323', monospace; color: var(--ink);}
.vn-next {position: absolute; right: 1rem; bottom: .5rem; color: var(--gold); font-size: 1rem; animation: blink 1s steps(2) infinite;}
@keyframes blink {50% {opacity: 0;}}
/* ---------- evidence / action cards ---------- */
.evidence {
  display: flex; gap: .9rem; align-items: flex-start; margin: .6rem 0;
  padding: .8rem 1rem; background: #241c40; border: 4px solid #5b5390; box-shadow: 5px 5px 0 var(--black);
}
.evidence-tag {
  flex: none; padding: .45rem .5rem; background: var(--gold); color: var(--black);
  font: .5rem 'Press Start 2P', monospace; border: 3px solid var(--black);
}
.evidence-text {font: 1.4rem/1.25 'VT323', monospace; color: var(--ink);}
.section-label {font: .6rem 'Press Start 2P', monospace; color: var(--gold); margin: 1.2rem 0 .3rem;}
/* ---------- verdict stamp ---------- */
.verdict {
  text-align: center; padding: 1.2rem 1rem; margin: 1.4rem 0 1rem;
  background: var(--black); border: 4px solid var(--gold); outline: 4px solid var(--black);
  box-shadow: 8px 8px 0 var(--black); animation: stamp .45s steps(5) both;
}
.verdict.fail {border-color: var(--red);}
.verdict-word {font: clamp(1.3rem, 4vw, 2.3rem) 'Press Start 2P', monospace; color: var(--gold); text-shadow: 4px 4px 0 #6b4a10;}
.verdict.fail .verdict-word {color: #ff7a7a; text-shadow: 4px 4px 0 #5a1a1f;}
.verdict p {margin: .8rem 0 0;}
@keyframes stamp {from {transform: scale(1.6); opacity: 0;} to {transform: scale(1); opacity: 1;}}
/* ---------- widgets ---------- */
.stButton>button {
  background: var(--red) !important; color: #fff !important;
  border: 4px solid var(--black) !important; border-radius: 0 !important;
  box-shadow: inset -4px -4px 0 #8f2835, inset 4px 4px 0 #ff8a8f, 4px 4px 0 var(--black) !important;
  min-height: 3rem; transition: none !important;
}
.stButton>button p {font-family: 'Press Start 2P', monospace !important; font-size: .62rem !important; line-height: 1.6 !important;}
.stButton>button:hover {filter: brightness(1.12);}
.stButton>button:active {transform: translate(4px, 4px); box-shadow: inset -4px -4px 0 #8f2835 !important;}
.stButton>button:disabled {background: #4a4466 !important; box-shadow: 4px 4px 0 var(--black) !important; color: #a9a3c4 !important;}
.stTextInput input, .stTextArea textarea {
  background: #0b0a18 !important; color: var(--ink) !important;
  border: 4px solid #5b5390 !important; border-radius: 0 !important;
  font: 1.35rem 'VT323', monospace !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {border-color: var(--gold) !important;}
.small-note {color: #9d96bf !important; font: 1.1rem 'VT323', monospace !important;}
hr {border-color: #3a335c !important;}
</style>
""", unsafe_allow_html=True)

# =====================================================================
#  PIXEL SPRITES  (original characters, drawn as character grids)
#  Each letter is one pixel; "." is transparent.
# =====================================================================
SPRITES = {
    # Prosecutor: dark bob haircut, round glasses, teal blazer
    "prosecutor": {
        "grid": [
            "....kkkkkkkk....",
            "...khhhhhhhhk...",
            "..khhhhhhhhhhk..",
            "..khsssssssshk..",
            "..khgegssgeghk..",
            "..khsssssssshk..",
            "..khhssSSsshhk..",
            "..khhsskksshhk..",
            "..khhhsssshhhk..",
            "..kkhhhsshhhkk..",
            "....kkkSSkkk....",
            "...kccwwwwcck...",
            "..kcccwttwccck..",
            ".kccccwttwcccck.",
            ".kcCcccwwcccCck.",
            "kcccCccccccCccck",
            "kcccCccccccCccck",
            "kcccCccccccCccck",
            "kkkkkkkkkkkkkkkk",
        ],
        "palette": {
            "k": "#05060c", "h": "#2b2238", "s": "#f1c7a0", "S": "#d39f78",
            "g": "#e8e8f0", "e": "#05060c", "c": "#2f9e98", "C": "#1f6f6b",
            "w": "#f4f1e8", "t": "#d8434b",
        },
    },
    # Defense: mustard beanie, orange hair, green hoodie
    "defense": {
        "grid": [
            "................",
            "....kkkkkkkk....",
            "...kbbbbbbbbk...",
            "..kbbbbbbbbbbk..",
            "..kBBBBBBBBBBk..",
            "..khsssssssshk..",
            "..khsesssseshk..",
            "..khsssssssshk..",
            "..khsksssskshk..",
            "..kssskkkksssk..",
            "...kssssssssk...",
            "....kksssskk....",
            "...kddkkkkddk...",
            "..kddddwwddddk..",
            ".kdddddwwdddddk.",
            "kddDdddwwdddDddk",
            "kddDddddddddDddk",
            "kddDddPPPPddDddk",
            "kkkkkkkkkkkkkkkk",
        ],
        "palette": {
            "k": "#05060c", "b": "#e0a33a", "B": "#a8701c", "h": "#d9772b",
            "s": "#f6d2ae", "S": "#d9a985", "e": "#05060c", "d": "#4f9a4b",
            "D": "#356b33", "w": "#f4f1e8", "P": "#356b33",
        },
    },
    # The Judge: a robot (it's the Court of AI, after all)
    "judge": {
        "grid": [
            ".......kk.......",
            ".......aa.......",
            ".......kk.......",
            "...kkkkkkkkkk...",
            "..kmmmmmmmmmmk..",
            "..kmkkkkkkkkmk..",
            "..kmkvvvvvvkmk..",
            "..kmkvavvavkmk..",
            "..kmkkkkkkkkmk..",
            "..kmmmmmmmmmmk..",
            "..kmmMkMkMkmmk..",
            "...kkkkkkkkkk...",
            "......kMMk......",
            "...krrwwwwrrk...",
            "..krrrwyywrrrk..",
            ".krrrrrwwrrrrrk.",
            "krrRrrrrrrrrRrrk",
            "krrRrrrrrrrrRrrk",
            "kkkkkkkkkkkkkkkk",
        ],
        "palette": {
            "k": "#05060c", "a": "#ffcf4a", "m": "#a9bccf", "M": "#6d8197",
            "v": "#12304a", "r": "#2a2340", "R": "#1b1630", "w": "#f4f1e8",
            "y": "#f2c14e",
        },
    },
}


@st.cache_data
def sprite_uri(name):
    """Turn a character grid into a crisp SVG data URI."""
    sprite = SPRITES[name]
    grid, palette = sprite["grid"], sprite["palette"]
    rects = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch != ".":
                rects.append(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{palette[ch]}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {len(grid[0])} {len(grid)}" '
           f'shape-rendering="crispEdges">{"".join(rects)}</svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def sprite_tag(name, left="50%", scale=11, extra_class=""):
    grid = SPRITES[name]["grid"]
    w, h = len(grid[0]) * scale, len(grid) * scale
    return (f'<img class="sprite {extra_class}" src="{sprite_uri(name)}" width="{w}" height="{h}" '
            f'style="left:{left}" alt="{name}">')


def esc(text):
    """Escape user / AI text so it can't break the HTML layout."""
    return html.escape(str(text)).replace("\n", "<br>")


CAST = {
    "pros": {
        "sprite": "prosecutor", "name": "ADA QUILL", "role": "PROSECUTOR",
        "bio": "Represents Person A. Sharp, precise, and never misses a detail.",
    },
    "def": {
        "sprite": "defense", "name": "RORY FINCH", "role": "DEFENSE",
        "bio": "Represents Person B. Laid-back, but always hears out every side.",
    },
    "judge": {
        "sprite": "judge", "name": "JUDGE AI-9", "role": "THE COURT",
        "bio": "A fair-minded robot judge. Weighs both sides and proposes a resolution.",
    },
}


def card_html(who, big=False):
    info = CAST[who]
    return (f'<div class="card {who}{" big" if big else ""}">'
            f'<div class="card-portrait">{sprite_tag(info["sprite"], scale=10)}</div>'
            f'<div class="card-name">{info["name"]}<br><span>{info["role"]}</span></div>'
            f'<div class="card-bio">{info["bio"]}</div></div>')


def link_html(label, down=False):
    return (f'<div class="link{" down" if down else ""}"><div class="link-label">{label}</div>'
            f'<div class="link-line"></div></div>')


def cast_map():
    """Opening-screen relationship map of the court's cast."""
    st.markdown(
        '<div class="courtroom"><div class="map-title">★ CAST OF THE COURT ★</div>'
        '<div class="map-row">' + card_html("pros") + link_html("OPPOSING<br>COUNSEL") + card_html("def") + '</div>'
        '<div class="map-row">' + link_html("BOTH ARGUE<br>BEFORE", down=True) + '</div>'
        '<div class="map-row">' + card_html("judge") + '</div></div>',
        unsafe_allow_html=True,
    )


TAG_COLORS = {"pros": "#8a3fae", "def": "#2f6fca", "judge": "#c9771c"}


def dialogue_html(speaker, text, kind="judge"):
    return (f'<div class="vn-box" style="--tag:{TAG_COLORS[kind]}">'
            f'<div class="vn-name">{esc(speaker)}</div>'
            f'<div class="vn-text">{esc(text)}</div><div class="vn-next">▼</div></div>')


def dialogue(speaker, text, kind="judge"):
    st.markdown(dialogue_html(speaker, text, kind), unsafe_allow_html=True)


def stage(who, text):
    """A speaker's portrait card beside their dialogue box, in the courtroom."""
    st.markdown(
        f'<div class="courtroom"><div class="stage-row">{card_html(who, big=True)}'
        f'<div class="vn-col">{dialogue_html(CAST[who]["name"], text, who)}</div></div></div>',
        unsafe_allow_html=True,
    )

def evidence_cards(plan):
    for index, step in enumerate(plan, 1):
        st.markdown(
            f'<div class="evidence"><div class="evidence-tag">#{index:02d}</div>'
            f'<div class="evidence-text">{esc(step)}</div></div>',
            unsafe_allow_html=True,
        )


def tracker(stage):
    steps = [("PROSECUTION", "1 PROSECUTE"), ("DEFENSE", "2 DEFEND"),
             ("RESOLUTION", "3 RULING"), ("AGREEMENT", "4 AGREE"), ("VERDICT", "5 VERDICT")]
    keys = [key for key, _ in steps]
    now = keys.index(stage)
    pips = "".join(
        f'<div class="pip {"now" if i == now else "done" if i < now else ""}">{label}</div>'
        for i, (_, label) in enumerate(steps)
    )
    st.markdown(f'<div class="tracker">{pips}</div>', unsafe_allow_html=True)


# =====================================================================
#  BACKEND + GAME LOGIC
# =====================================================================
try:
    from court_ai import generate_trial
    BACKEND_AVAILABLE = True
except ImportError:
    generate_trial = None
    BACKEND_AVAILABLE = False

try:
    from court_logic import MAX_ROUNDS
except ImportError:
    MAX_ROUNDS = 3

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
            "Both: Ask before taking food or belongings that may belong to someone else.",
        ],
    }


def init_state():
    defaults = {
        "case": None, "stage": "SUBMIT", "trial": None, "round": 1,
        "choices": {"a": None, "b": None}, "demo_mode": not BACKEND_AVAILABLE,
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
    if not a or not b:
        if not a:
            st.error("Person A's statement is required.")
        if not b:
            st.error("Person B's statement is required.")
        return
    # Remember demo mode now: the checkbox disappears once the trial starts.
    st.session_state.demo_mode = st.session_state.get("use_demo", not BACKEND_AVAILABLE)
    try:
        trial = validate_trial(make_trial(a, b, st.session_state.demo_mode))
    except Exception as exc:
        message = str(exc)
        if "11434" in message or "connection" in message.lower() or "refused" in message.lower():
            st.error("The court cannot reach Ollama. Make sure Ollama is running and the model is installed.")
        else:
            st.error(f"Could not start the trial: {message}")
        return
    st.session_state.case = {"title": title or "Untitled Case", "person_a": a, "person_b": b}
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
    a, b = st.session_state.case["person_a"], st.session_state.case["person_b"]
    previous = st.session_state.trial["resolution"]
    feedback = st.session_state.get("appeal_feedback", "").strip()
    try:
        if st.session_state.demo_mode:
            updated = validate_trial(demo_trial(a, b))
        else:
            updated = validate_trial(generate_trial(a, b, previous_resolution=previous, appeal_feedback=feedback))
    except Exception as exc:
        st.error(f"The court could not prepare another resolution: {exc}")
        return
    st.session_state.round += 1
    st.session_state.trial["resolution"] = updated["resolution"]
    st.session_state.trial["action_plan"] = updated["action_plan"]
    st.session_state.choices = {"a": None, "b": None}
    st.session_state.stage = "RESOLUTION"


# =====================================================================
#  SCREENS
# =====================================================================
init_state()

st.markdown(
    '<div class="hero"><div class="hero-kicker">★ THE PEOPLE\'S COURT · EST. 2026 ★</div>'
    '<div class="hero-title">COURT OF AI</div>'
    '<div class="hero-sub">Your side of the story is now in session.</div></div>',
    unsafe_allow_html=True,
)

if st.session_state.case is None:
    # ---------------- Case submission ----------------
    st.markdown('<div class="case-strip">CASE FILE 001 · NEW MATTER · AWAITING STATEMENTS</div>', unsafe_allow_html=True)
    cast_map()
    dialogue("JUDGE AI-9", "Order, order! Every great trial starts with two sides. "
             "Present both statements, and this court will hear the arguments, weigh a compromise, "
             "and issue an action plan.")

    st.text_input("Case title (optional)", key="in_title", placeholder="e.g. The Case of the Stolen Snacks")
    left, right = st.columns(2)
    with left:
        st.markdown("### 🟪 PERSON A")
        st.text_area("What happened from Person A's perspective?", key="in_claim_a", height=160,
                     placeholder="Explain what happened and why you're upset...")
    with right:
        st.markdown("### 🟦 PERSON B")
        st.text_area("What happened from Person B's perspective?", key="in_claim_b", height=160,
                     placeholder="Explain your side of the story...")
    st.checkbox("Use Demo Mode (no Ollama required)", key="use_demo", value=not BACKEND_AVAILABLE)
    c1, c2 = st.columns(2)
    with c1:
        st.button("Load Sample Case", key="load_sample", use_container_width=True,
                  on_click=lambda: st.session_state.update({
                      "in_title": SAMPLE_TITLE, "in_claim_a": SAMPLE_A, "in_claim_b": SAMPLE_B}))
    with c2:
        st.button("⚖ Start Trial", key="start", use_container_width=True, on_click=start_trial)
    st.markdown('<p class="small-note">COURT NOTICE: The AI mediator is not a real judge. '
                'Keep statements respectful and avoid sharing private information.</p>', unsafe_allow_html=True)

else:
    case = st.session_state.case
    trial = st.session_state.trial
    stage_name = st.session_state.stage

    st.markdown(f'<div class="case-strip">CASE FILE · {esc(case["title"].upper())} · '
                f'ROUND {st.session_state.round}/{MAX_ROUNDS}</div>', unsafe_allow_html=True)
    tracker(stage_name)

    if stage_name == "PROSECUTION":
        stage("pros", trial["prosecutor"])
        st.button("Hear the defense ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "DEFENSE":
        stage("def", trial["defense"])
        st.button("Approach the bench ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "RESOLUTION":
        stage("judge", trial["resolution"])
        plan = trial.get("action_plan", [])
        if plan:
            st.markdown('<div class="section-label">📜 COURT-ORDERED ACTION PLAN</div>', unsafe_allow_html=True)
            evidence_cards(plan)
        st.button("Proceed to agreement ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "AGREEMENT":
        st.markdown('<div class="courtroom"><div class="duo">' + card_html("pros") + card_html("def")
                    + '</div></div>', unsafe_allow_html=True)
        dialogue("JUDGE AI-9", "Both parties must now decide: do you accept the proposed resolution? "
                 "The verdict will be revealed once both have answered.")
        a_col, b_col = st.columns(2)
        for col, side, label in ((a_col, "a", "🟪 PERSON A"), (b_col, "b", "🟦 PERSON B")):
            with col:
                st.markdown(f"### {label}")
                locked = st.session_state.choices[side] is not None
                st.button("✓ Accept", key=f"accept_{side}", disabled=locked, on_click=choose,
                          args=(side, "accept"), use_container_width=True)
                st.button("✕ Decline", key=f"decline_{side}", disabled=locked, on_click=choose,
                          args=(side, "decline"), use_container_width=True)
                if locked:
                    st.caption(f"Answer recorded: {st.session_state.choices[side].upper()}")
        if all(st.session_state.choices.values()):
            st.button("⚖ Reveal Verdict", key="see_verdict", use_container_width=True,
                      on_click=lambda: st.session_state.update({"stage": "VERDICT"}))

    elif stage_name == "VERDICT":
        accepted = all(value == "accept" for value in st.session_state.choices.values())
        if accepted:
            stage("judge", "The parties have accepted the court's resolution. This case is settled!")
            st.markdown('<div class="verdict"><div class="verdict-word">CASE SETTLED</div></div>',
                        unsafe_allow_html=True)
            st.markdown('<div class="section-label">📜 FINAL ACTION PLAN</div>', unsafe_allow_html=True)
            evidence_cards(trial.get("action_plan", []))
        else:
            if st.session_state.round < MAX_ROUNDS:
                stage("judge", "The proposed resolution was not accepted by both parties. The court will hear an appeal.")
            else:
                stage("judge", "The proposed resolution was not accepted by both parties, "
                               "and this court has run out of attempts.")
            st.markdown('<div class="verdict fail"><div class="verdict-word">NO DEAL</div></div>',
                        unsafe_allow_html=True)
            if st.session_state.round < MAX_ROUNDS:
                st.text_area("Why was the ruling rejected? (optional)", key="appeal_feedback",
                             placeholder="Explain what the judge got wrong...", height=110)
                st.button("Request revised ruling", key="retry", on_click=retry_resolution,
                          use_container_width=True)
            else:
                st.warning("The court has reached its maximum number of resolution attempts.")
        st.button("Start a new trial", key="reset_verdict", on_click=reset_trial, use_container_width=True)

    with st.expander("📁 View submitted statements", expanded=False):
        a_col, b_col = st.columns(2)
        with a_col:
            st.markdown("**PERSON A**")
            st.write(case["person_a"])
        with b_col:
            st.markdown("**PERSON B**")
            st.write(case["person_b"])

    st.divider()
    if stage_name != "VERDICT":
        st.button("↺ Abandon case / New trial", key="reset_sidebar", on_click=reset_trial)
    st.markdown('<p class="small-note">COURT OF AI · A fictional mediation experience, not legal advice.</p>',
                unsafe_allow_html=True)