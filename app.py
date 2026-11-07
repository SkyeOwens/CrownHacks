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
#  STYLING: light, sunny courtroom with blocky pixel details
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
:root {
  --ink: #3a2a1a;
  --brown: #6b3a16;
  --dark: #2b1a0e;
  --gold: #c98a2e;
  --cream: #fffaf0;
  --line: #c9a36b;
  --red: #c8413f;
}
.stApp {
  background-color: #f4ecdc;
  background-image:
    linear-gradient(rgba(107,58,22,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(107,58,22,.05) 1px, transparent 1px);
  background-size: 8px 8px;
  color: var(--ink);
}
.block-container {max-width: 1000px; padding-top: 1.2rem; padding-bottom: 3rem;}
.stApp p, .stApp label, .stApp li, .stMarkdown {font-family: 'VT323', monospace; font-size: 1.3rem; color: var(--ink);}
h1, h2, h3 {font-family: 'Press Start 2P', monospace !important; color: var(--brown) !important;}
h3 {font-size: .9rem !important; line-height: 1.6 !important;}
/* ---------- title card ---------- */
.hero {
  text-align: center; padding: 1.3rem 1rem 1.1rem; margin-bottom: 1rem;
  background: var(--cream); border: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark);
}
.hero-kicker {font: .58rem 'Press Start 2P', monospace; color: var(--gold); letter-spacing: .18em;}
.hero-title {
  font: clamp(1.5rem, 5vw, 2.6rem) 'Press Start 2P', monospace; color: var(--red);
  margin: .85rem 0 .6rem; text-shadow: 4px 4px 0 var(--dark);
}
.hero-sub {font: 1.45rem 'VT323', monospace; color: #7a5a3a;}
/* ---------- case strip + stage tracker ---------- */
.case-strip {
  background: var(--cream); border: 4px solid var(--line); border-left: 12px solid var(--gold);
  padding: .6rem 1rem; margin: .3rem 0 .8rem; font: .6rem/1.7 'Press Start 2P', monospace; color: var(--brown);
}
.tracker {display: flex; gap: 6px; margin: 0 0 1rem; flex-wrap: wrap;}
.pip {
  flex: 1; min-width: 110px; text-align: center; padding: .5rem .3rem;
  font: .5rem 'Press Start 2P', monospace; color: #a88c68; background: #efe3c9; border: 3px solid var(--line);
}
.pip.done {color: var(--brown);}
.pip.now {color: #fff; background: var(--gold); border-color: var(--dark); box-shadow: 3px 3px 0 var(--dark);}
/* =========================== THE COURTROOM =========================== */
.court {
  position: relative; height: 470px; overflow: hidden; margin: .2rem 0 0;
  border: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark);
  background:
    linear-gradient(#8a5a2e, #8a5a2e) 0 312px / 100% 8px no-repeat,
    repeating-linear-gradient(90deg, #b07a46 0 6px, #c99360 6px 74px, #b07a46 74px 80px) 0 222px / 100% 90px no-repeat,
    linear-gradient(#7a4a24, #7a4a24) 0 214px / 100% 8px no-repeat,
    repeating-linear-gradient(180deg, rgba(150,120,80,.10) 0 2px, transparent 2px 24px) 0 0 / 100% 214px no-repeat,
    linear-gradient(180deg, #f6efe0, #ebdfc6) 0 0 / 100% 214px no-repeat,
    #e9dcc0;
}
/* tiled floor in perspective */
.floor {
  position: absolute; left: -40%; right: -40%; bottom: -10px; height: 470px;
  transform: perspective(380px) rotateX(58deg); transform-origin: 50% 100%;
  background: repeating-conic-gradient(#f7eedb 0 25%, #d8c19a 0 50%) 0 0 / 120px 120px;
  box-shadow: inset 0 60px 40px -20px rgba(90,60,30,.25);
}
/* beamed ceiling + hanging lamps */
.ceiling {
  position: absolute; top: 0; left: 0; right: 0; height: 30px; z-index: 3;
  background: repeating-linear-gradient(90deg, #6e4020 0 10px, #9a6232 10px 70px);
  border-bottom: 5px solid var(--dark);
}
.lamp {position: absolute; top: 30px; width: 4px; height: 46px; background: var(--dark); transform: translateX(-50%); z-index: 3;}
.lamp::after {
  content: ""; position: absolute; left: 50%; top: 44px; width: 44px; height: 20px; transform: translateX(-50%);
  background: #f2c14e; border: 4px solid var(--dark); border-radius: 22px 22px 4px 4px;
  box-shadow: 0 18px 30px 6px rgba(255,220,130,.55);
}
/* tall arched window behind the judge */
.arch {
  position: absolute; top: 40px; left: 50%; width: 300px; height: 220px; transform: translateX(-50%);
  border: 8px solid #9a6232; border-bottom: none; border-radius: 150px 150px 0 0;
  background:
    linear-gradient(90deg, transparent 0 calc(33% - 3px), #b98a52 calc(33% - 3px) calc(33% + 3px), transparent calc(33% + 3px) calc(67% - 3px), #b98a52 calc(67% - 3px) calc(67% + 3px), transparent calc(67% + 3px)),
    repeating-linear-gradient(180deg, transparent 0 46px, #b98a52 46px 52px),
    linear-gradient(180deg, #fff3c8, #cfe7fb 45%, #b5d6f3);
  box-shadow: inset 0 0 0 4px #e7c98e, 0 0 0 4px var(--dark);
}
.pillar {
  position: absolute; top: 30px; height: 190px; width: 44px; transform: translateX(-50%); z-index: 0;
  background: repeating-linear-gradient(90deg, #e2d6bb 0 4px, #fbf6ea 4px 10px);
  border-left: 4px solid #bfae8a; border-right: 4px solid #bfae8a;
}
.pillar::before, .pillar::after {content: ""; position: absolute; left: -12px; right: -12px; height: 14px; background: #e9dec5; border: 4px solid #bfae8a;}
.pillar::before {top: 0;} .pillar::after {bottom: -4px;}
/* stations: each character's spot in the room */
.station {position: absolute; top: 0; bottom: 0; width: 220px; transform: translateX(-50%); transition: filter .2s;}
.station.dim {filter: brightness(.72) saturate(.55);}
.station .who {position: absolute; left: 50%; transform: translateX(-50%); image-rendering: pixelated;}
.station.active .who {animation: talk .8s steps(2) infinite;}
@keyframes talk {50% {transform: translate(-50%, -4px);}}
.station.active::before {
  content: ""; position: absolute; left: 50%; bottom: 10px; width: 260px; height: 60px; transform: translateX(-50%);
  background: radial-gradient(ellipse at center, rgba(255,240,170,.75), transparent 70%);
}
/* lawyer podiums */
.podium {
  position: absolute; left: 50%; bottom: 36px; width: 190px; height: 124px; transform: translateX(-50%);
  background: linear-gradient(180deg, #c98d55 0 14px, #9a6232 14px 20px, #b87a44 20px 100%);
  border: 4px solid var(--dark); box-shadow: inset 10px 0 0 rgba(255,255,255,.08), inset -10px 0 0 rgba(0,0,0,.12);
}
.podium::after {content: ""; position: absolute; left: 14px; right: 14px; top: 30px; bottom: 14px; border: 4px solid #9a6232;}
.plate {
  position: absolute; left: 50%; transform: translateX(-50%); z-index: 2; white-space: nowrap; text-align: center;
  padding: .35rem .55rem; background: #f2d48a; color: var(--dark); border: 3px solid var(--dark);
  font: .45rem/1.7 'Press Start 2P', monospace;
}
.station.active .plate {background: #ffe7a3; box-shadow: 0 0 0 3px #fff3c4, 0 0 14px 4px rgba(255,214,102,.9);}
.podium .plate {top: 46px;}
/* judge: tall chair + raised bench */
.chair {
  position: absolute; left: 50%; bottom: 218px; width: 184px; height: 228px; transform: translateX(-50%);
  background: linear-gradient(90deg, #6e2626 0 12px, #8e3434 12px 172px, #6e2626 172px);
  border: 4px solid var(--dark); border-radius: 46px 46px 0 0;
  box-shadow: inset 0 0 0 6px #b8862e;
}
.bench {
  position: absolute; left: 50%; bottom: 122px; width: 40%; min-width: 330px; height: 168px; transform: translateX(-50%); z-index: 1;
  background: linear-gradient(180deg, #d39a5f 0 16px, #9a6232 16px 24px, #bf8148 24px 100%);
  border: 4px solid var(--dark);
}
.bench::before {
  content: ""; position: absolute; left: 18px; right: 18px; top: 38px; bottom: 16px;
  border: 4px solid #9a6232; box-shadow: inset 0 0 0 4px #c98d55;
}
.seal {
  position: absolute; left: 50%; top: 52px; width: 64px; height: 64px; transform: translateX(-50%);
  display: flex; align-items: center; justify-content: center; font-size: 2rem; z-index: 1;
  background: #f2c14e; border: 4px solid var(--dark); border-radius: 50%; box-shadow: inset 0 0 0 5px #c98a2e;
}
.bench .plate {top: auto; bottom: 18px;}
.dais {
  position: absolute; left: 50%; bottom: 96px; width: 50%; min-width: 400px; height: 30px; transform: translateX(-50%); z-index: 1;
  background: linear-gradient(180deg, #d9a96f 0 12px, #a8743f 12px 15px, #c99360 15px 100%);
  border: 4px solid var(--dark);
}
.judge-station .who {bottom: 268px;}
.lawyer-station .who {bottom: 122px;}
/* ---------- visual-novel dialogue box ---------- */
.vn-box {
  position: relative; margin: 1.8rem 0 1.1rem; padding: 1.7rem 1.4rem 1.6rem;
  background: rgba(24, 20, 40, .96); border: 4px solid #fff; outline: 4px solid var(--dark);
  box-shadow: 8px 8px 0 var(--dark);
}
.vn-name {
  position: absolute; top: -1.35rem; left: 1rem; padding: .5rem .8rem;
  font: .62rem 'Press Start 2P', monospace; color: #fff; background: var(--tag, var(--gold));
  border: 4px solid #fff; outline: 4px solid var(--dark);
}
.stApp .vn-text {font: 1.6rem/1.3 'VT323', monospace; color: #f6f1e4;}
.vn-next {position: absolute; right: 1rem; bottom: .5rem; color: #f2c14e; font-size: 1rem; animation: blink 1s steps(2) infinite;}
@keyframes blink {50% {opacity: 0;}}
/* ---------- action-plan cards ---------- */
.evidence {
  display: flex; gap: .9rem; align-items: flex-start; margin: .6rem 0; padding: .8rem 1rem;
  background: var(--cream); border: 4px solid var(--line); box-shadow: 5px 5px 0 var(--dark);
}
.evidence-tag {flex: none; padding: .45rem .5rem; background: var(--gold); color: #fff; font: .5rem 'Press Start 2P', monospace; border: 3px solid var(--dark);}
.stApp .evidence-text {font: 1.4rem/1.25 'VT323', monospace; color: var(--ink);}
.section-label {font: .6rem 'Press Start 2P', monospace; color: var(--brown); margin: 1.2rem 0 .3rem;}
/* ---------- verdict stamp ---------- */
.verdict {
  text-align: center; padding: 1.2rem 1rem; margin: 1.4rem 0 1rem; background: var(--cream);
  border: 6px double var(--gold); box-shadow: 8px 8px 0 var(--dark); animation: stamp .45s steps(5) both;
}
.verdict.fail {border-color: var(--red);}
.verdict-word {font: clamp(1.3rem, 4vw, 2.3rem) 'Press Start 2P', monospace; color: #3f8a3a; text-shadow: 4px 4px 0 var(--dark);}
.verdict.fail .verdict-word {color: var(--red);}
@keyframes stamp {from {transform: scale(1.6); opacity: 0;} to {transform: scale(1); opacity: 1;}}
/* ---------- widgets ---------- */
.stButton>button {
  background: var(--red) !important; color: #fff !important;
  border: 4px solid var(--dark) !important; border-radius: 0 !important;
  box-shadow: inset -4px -4px 0 #8f2835, inset 4px 4px 0 #ff8a8f, 4px 4px 0 var(--dark) !important;
  min-height: 3rem; transition: none !important;
}
.stButton>button p {font-family: 'Press Start 2P', monospace !important; font-size: .62rem !important; line-height: 1.6 !important; color: #fff !important;}
.stButton>button:hover {filter: brightness(1.1);}
.stButton>button:active {transform: translate(4px, 4px); box-shadow: inset -4px -4px 0 #8f2835 !important;}
.stButton>button:disabled {background: #cdbb9c !important; box-shadow: 4px 4px 0 var(--dark) !important;}
.stTextInput input, .stTextArea textarea {
  background: #fffdf7 !important; color: var(--dark) !important;
  border: 4px solid var(--line) !important; border-radius: 0 !important;
  font: 1.35rem 'VT323', monospace !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {border-color: var(--gold) !important;}
.small-note {color: #8a7356 !important; font: 1.1rem 'VT323', monospace !important;}
hr {border-color: var(--line) !important;}
@media (max-width: 760px) {
  .court {height: 360px;}
  .station {transform: translateX(-50%) scale(.7); transform-origin: bottom center;}
  .bench {transform: translateX(-50%) scale(.75); transform-origin: bottom center;}
  .chair {display: none;}
}
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


def sprite_tag(name, scale=9):
    grid = SPRITES[name]["grid"]
    return (f'<img class="who" src="{sprite_uri(name)}" width="{len(grid[0]) * scale}" '
            f'height="{len(grid) * scale}" alt="{name}">')


def esc(text):
    """Escape user / AI text so it can't break the HTML layout."""
    return html.escape(str(text)).replace("\n", "<br>")


CAST = {
    "def":   {"sprite": "defense",    "name": "RORY FINCH", "role": "DEFENSE",    "color": "#2f6fca"},
    "pros":  {"sprite": "prosecutor", "name": "ADA QUILL",  "role": "PROSECUTION", "color": "#8a3fae"},
    "judge": {"sprite": "judge",      "name": "JUDGE AI-9", "role": "THE COURT",  "color": "#c9771c"},
}


def courtroom(active=()):
    """Draw the whole courtroom. `active` lists who is lit up; everyone else dims.
    Defense on the left, the judge raised in the middle, prosecution on the right."""
    active = set(active)

    def state(who):
        if not active:
            return ""
        return " active" if who in active else " dim"

    def lawyer(who, left):
        c = CAST[who]
        return (f'<div class="station lawyer-station{state(who)}" style="left:{left}">'
                f'{sprite_tag(c["sprite"])}'
                f'<div class="podium"><div class="plate">{c["role"]}<br>{c["name"]}</div></div></div>')

    j = CAST["judge"]
    room = (
        '<div class="court"><div class="floor"></div>'
        '<div class="ceiling"></div><div class="lamp" style="left:20%"></div><div class="lamp" style="left:80%"></div>'
        '<div class="pillar" style="left:27%"></div><div class="pillar" style="left:36%"></div>'
        '<div class="pillar" style="left:64%"></div><div class="pillar" style="left:73%"></div>'
        '<div class="arch"></div>'
        # judge (chair + sprite live in a station so they dim together)
        f'<div class="station judge-station{state("judge")}" style="left:50%; width:260px">'
        f'<div class="chair"></div>{sprite_tag(j["sprite"])}</div>'
        f'<div class="dais"></div><div class="bench{state("judge").replace("active", "")}"><div class="seal">⚖</div>'
        f'<div class="plate">{j["name"]}</div></div>'
        + lawyer("def", "13%")
        + lawyer("pros", "87%")
        + '</div>'
    )
    st.markdown(room, unsafe_allow_html=True)


def dialogue(who, text):
    c = CAST[who]
    st.markdown(
        f'<div class="vn-box" style="--tag:{c["color"]}">'
        f'<div class="vn-name">{c["name"]} · {c["role"]}</div>'
        f'<div class="vn-text">{esc(text)}</div><div class="vn-next">▼</div></div>',
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
    now = [key for key, _ in steps].index(stage)
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
    courtroom()
    dialogue("judge", "Order, order! Every great trial starts with two sides. "
             "Present both statements, and this court will hear the arguments, weigh a compromise, "
             "and issue an action plan.")

    st.text_input("Case title (optional)", key="in_title", placeholder="e.g. The Case of the Stolen Snacks")
    left, right = st.columns(2)
    with left:
        st.markdown("### 🟦 PERSON B")
        st.text_area("What happened from Person B's perspective? (represented by the Defense)", key="in_claim_b",
                     height=160, placeholder="Explain your side of the story...")
    with right:
        st.markdown("### 🟪 PERSON A")
        st.text_area("What happened from Person A's perspective? (represented by the Prosecution)", key="in_claim_a",
                     height=160, placeholder="Explain what happened and why you're upset...")
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
        courtroom(active=["pros"])
        dialogue("pros", trial["prosecutor"])
        st.button("Hear the defense ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "DEFENSE":
        courtroom(active=["def"])
        dialogue("def", trial["defense"])
        st.button("Approach the bench ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "RESOLUTION":
        courtroom(active=["judge"])
        dialogue("judge", trial["resolution"])
        plan = trial.get("action_plan", [])
        if plan:
            st.markdown('<div class="section-label">📜 COURT-ORDERED ACTION PLAN</div>', unsafe_allow_html=True)
            evidence_cards(plan)
        st.button("Proceed to agreement ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "AGREEMENT":
        courtroom(active=["def", "pros"])
        dialogue("judge", "Both parties must now decide: do you accept the proposed resolution? "
                 "The verdict will be revealed once both have answered.")
        b_col, a_col = st.columns(2)  # Person B on the left with the Defense, A on the right
        for col, side, label in ((b_col, "b", "🟦 PERSON B"), (a_col, "a", "🟪 PERSON A")):
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
        courtroom(active=["judge"])
        accepted = all(value == "accept" for value in st.session_state.choices.values())
        if accepted:
            dialogue("judge", "The parties have accepted the court's resolution. This case is settled!")
            st.markdown('<div class="verdict"><div class="verdict-word">CASE SETTLED</div></div>',
                        unsafe_allow_html=True)
            st.markdown('<div class="section-label">📜 FINAL ACTION PLAN</div>', unsafe_allow_html=True)
            evidence_cards(trial.get("action_plan", []))
        
        else:
            if st.session_state.round < MAX_ROUNDS:
                dialogue("judge", "The proposed resolution was not accepted by both parties. "
                                  "Very well, the court will attempt another resolution.")
            else:
                dialogue("judge", "The proposed resolution was not accepted by both parties, "
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
        b_col, a_col = st.columns(2)
        with b_col:
            st.markdown("**PERSON B**")
            st.write(case["person_b"])
        with a_col:
            st.markdown("**PERSON A**")
            st.write(case["person_a"])

    st.divider()
    if stage_name != "VERDICT":
        st.button("↺ Abandon case / New trial", key="reset_sidebar", on_click=reset_trial)
    st.markdown('<p class="small-note">COURT OF AI · A fictional mediation experience, not legal advice.</p>',
                unsafe_allow_html=True)
