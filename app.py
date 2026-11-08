import base64
import html
import inspect
import os
import random
import time

import streamlit as st

st.set_page_config(
    page_title="Court of AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from court_logic import (MAX_ROUNDS, ACHIEVEMENTS, THEMES, OUTFITS,
                         load_progress, save_progress, unlocked, record_verdict)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(APP_DIR, "assets")

# =====================================================================
#  STYLING
# =====================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323&display=swap');
:root {
  --ink: #3a2a1a; --brown: #6b3a16; --dark: #2b1a0e; --gold: #c98a2e;
  --cream: #fffaf0; --line: #c9a36b; --red: #c8413f;
}
.stApp {
  background-color: #f4ecdc;
  background-image:
    linear-gradient(rgba(107,58,22,.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(107,58,22,.05) 1px, transparent 1px);
  background-size: 8px 8px; color: var(--ink);
}
.block-container {max-width: 1000px; padding-top: 1.2rem; padding-bottom: 3rem;}
.stApp p, .stApp label, .stApp li, .stMarkdown {font-family: 'VT323', monospace; font-size: 1.3rem; color: var(--ink);}
h1, h2, h3 {font-family: 'Press Start 2P', monospace !important; color: var(--brown) !important;}
h3 {font-size: .9rem !important; line-height: 1.6 !important;}
/* ---------- title card ---------- */
.hero {text-align: center; padding: 1.3rem 1rem 1.1rem; margin-bottom: .6rem; background: var(--cream); border: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark);}
.hero-kicker {font: .58rem 'Press Start 2P', monospace; color: var(--gold); letter-spacing: .18em;}
.hero-title {font: clamp(1.5rem, 5vw, 2.6rem) 'Press Start 2P', monospace; color: var(--red); margin: .85rem 0 .6rem; text-shadow: 4px 4px 0 var(--dark);}
.hero-sub {font: 1.45rem 'VT323', monospace; color: #7a5a3a;}
/* ---------- case strip + stage tracker ---------- */
.case-strip {background: var(--cream); border: 4px solid var(--line); border-left: 12px solid var(--gold); padding: .6rem 1rem; margin: .3rem 0 .8rem; font: .6rem/1.7 'Press Start 2P', monospace; color: var(--brown);}
.tracker {display: flex; gap: 6px; margin: 0 0 1rem; flex-wrap: wrap;}
.pip {flex: 1; min-width: 110px; text-align: center; padding: .5rem .3rem; font: .5rem 'Press Start 2P', monospace; color: #a88c68; background: #efe3c9; border: 3px solid var(--line);}
.pip.done {color: var(--brown);}
.pip.now {color: #fff; background: var(--gold); border-color: var(--dark); box-shadow: 3px 3px 0 var(--dark);}

/* =========================== THE COURTROOM ===========================
   Colors live in variables so unlockable themes can swap them. */
.court {
  --wall1: #f6efe0; --wall2: #ebdfc6; --wain1: #b07a46; --wain2: #c99360; --trim: #7a4a24; --base: #8a5a2e;
  --tile1: #f7eedb; --tile2: #d8c19a; --floor-bg: #e9dcc0;
  --runner1: #b23a3a; --runner2: #a33333; --runner-edge: #e2b04a;
  position: relative; height: 560px; overflow: hidden; margin: .2rem 0 0;
  border: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark);
  background:
    linear-gradient(var(--base), var(--base)) 0 312px / 100% 8px no-repeat,
    repeating-linear-gradient(90deg, var(--wain1) 0 6px, var(--wain2) 6px 74px, var(--wain1) 74px 80px) 0 222px / 100% 90px no-repeat,
    linear-gradient(var(--trim), var(--trim)) 0 214px / 100% 8px no-repeat,
    repeating-linear-gradient(180deg, rgba(150,120,80,.10) 0 2px, transparent 2px 24px) 0 0 / 100% 214px no-repeat,
    linear-gradient(180deg, var(--wall1), var(--wall2)) 0 0 / 100% 214px no-repeat,
    var(--floor-bg);
}
.floor {
  position: absolute; left: -40%; right: -40%; bottom: -10px; height: 560px;
  transform: perspective(380px) rotateX(58deg); transform-origin: 50% 100%;
  background: repeating-conic-gradient(var(--tile1) 0 25%, var(--tile2) 0 50%) 0 0 / 120px 120px;
  box-shadow: inset 0 60px 40px -20px rgba(90,60,30,.25);
}
.runner {
  position: absolute; left: 50%; top: 0; bottom: 0; width: 230px; transform: translateX(-50%);
  background: repeating-linear-gradient(180deg, var(--runner1) 0 30px, var(--runner2) 30px 34px);
  border-left: 10px solid var(--runner-edge); border-right: 10px solid var(--runner-edge);
}
.ceiling {position: absolute; top: 0; left: 0; right: 0; height: 30px; z-index: 3; background: repeating-linear-gradient(90deg, #6e4020 0 10px, #9a6232 10px 70px); border-bottom: 5px solid var(--dark);}
.lamp {position: absolute; top: 30px; width: 4px; height: 46px; background: var(--dark); transform: translateX(-50%); z-index: 3;}
.lamp::after {content: ""; position: absolute; left: 50%; top: 44px; width: 44px; height: 20px; transform: translateX(-50%); background: #f2c14e; border: 4px solid var(--dark); border-radius: 22px 22px 4px 4px; box-shadow: 0 18px 30px 6px rgba(255,220,130,.55);}
.arch {
  position: absolute; top: 40px; left: 50%; width: 300px; height: 220px; transform: translateX(-50%);
  border: 8px solid #9a6232; border-bottom: none; border-radius: 150px 150px 0 0;
  background:
    linear-gradient(90deg, transparent 0 calc(33% - 3px), #b98a52 calc(33% - 3px) calc(33% + 3px), transparent calc(33% + 3px) calc(67% - 3px), #b98a52 calc(67% - 3px) calc(67% + 3px), transparent calc(67% + 3px)),
    repeating-linear-gradient(180deg, transparent 0 46px, #b98a52 46px 52px),
    linear-gradient(180deg, #fff3c8, #cfe7fb 45%, #b5d6f3);
  box-shadow: inset 0 0 0 4px #e7c98e, 0 0 0 4px var(--dark);
}
.pillar {position: absolute; top: 30px; height: 190px; width: 44px; transform: translateX(-50%); background: repeating-linear-gradient(90deg, #e2d6bb 0 4px, #fbf6ea 4px 10px); border-left: 4px solid #bfae8a; border-right: 4px solid #bfae8a;}
.pillar::before, .pillar::after {content: ""; position: absolute; left: -12px; right: -12px; height: 14px; background: #e9dec5; border: 4px solid #bfae8a;}
.pillar::before {top: 0;} .pillar::after {bottom: -4px;}
/* extra courtroom details: wall clock, motto plaque, front railing */
.clock {position: absolute; top: 92px; left: 9%; width: 54px; height: 54px; transform: translateX(-50%); background: #fffaf0; border: 5px solid #7a4a24; border-radius: 50%; box-shadow: 0 0 0 3px var(--dark);}
.clock::before {content: ""; position: absolute; left: calc(50% - 2px); top: 8px; width: 4px; height: 18px; background: var(--dark);}
.clock::after {content: ""; position: absolute; left: 50%; top: calc(50% - 2px); width: 14px; height: 4px; background: var(--red);}
.motto {position: absolute; top: 98px; left: 91%; transform: translateX(-50%); padding: .45rem .5rem; background: #7a4a24; color: #f2d48a; border: 4px solid var(--dark); font: .42rem/1.9 'Press Start 2P', monospace; text-align: center; white-space: nowrap;}
.railing {
  position: absolute; left: 0; right: 0; bottom: 0; height: 40px; z-index: 5; border-top: 4px solid var(--dark);
  background:
    linear-gradient(#8a5329, #8a5329) 0 0 / 100% 10px no-repeat,
    repeating-linear-gradient(90deg, transparent 0 24px, #a8693a 24px 34px, #8a5329 34px 36px, transparent 36px 48px) 0 10px / 100% 30px no-repeat;
}
/* ---------- the room's layout, back to front ----------
   back:   judge's bench (center) + an empty witness stand on each side + the jury box (right)
   front:  two counsel tables closest to you: Person A on the left, Person B on the right */
.station {position: absolute; top: 0; bottom: 0; width: 240px; transform: translateX(-50%);}
.station.dim {filter: brightness(.72) saturate(.55);}
.station .who {position: absolute; left: 50%; transform: translateX(-50%); image-rendering: pixelated; z-index: 1;}
@keyframes talk {50% {transform: translate(-50%, -4px);}}
/* spotlight: a cone of light from the ceiling onto whoever is speaking */
.station.active::before {
  content: ""; position: absolute; left: 50%; top: 30px; bottom: 0; width: 300px; transform: translateX(-50%); z-index: 0;
  background: linear-gradient(180deg, rgba(255,244,190,.65), rgba(255,236,160,.18) 85%, rgba(255,236,160,0));
  clip-path: polygon(42% 0, 58% 0, 100% 100%, 0 100%); pointer-events: none;
}
.station.active::after {content: ""; position: absolute; left: 50%; bottom: 4px; width: 280px; height: 50px; transform: translateX(-50%);
  background: radial-gradient(ellipse at center, rgba(255,240,170,.8), transparent 70%); pointer-events: none;}
.plate {position: absolute; left: 50%; transform: translateX(-50%); z-index: 2; white-space: nowrap; text-align: center; padding: .35rem .55rem; background: #f2d48a; color: var(--dark); border: 3px solid var(--dark); font: .45rem/1.7 'Press Start 2P', monospace;}
.station.active .plate {background: #ffe7a3; box-shadow: 0 0 0 3px #fff3c4, 0 0 14px 4px rgba(255,214,102,.9);}
/* judge: tall chair + raised bench + dais */
.judge-station {z-index: 3;}
.judge-station .who {bottom: 312px;}
.station.judge-station.active .who {animation: talk .8s steps(2) infinite;}
.chair {position: absolute; left: 50%; bottom: 290px; width: 176px; height: 200px; transform: translateX(-50%); background: linear-gradient(90deg, #6e2626 0 12px, #8e3434 12px 164px, #6e2626 164px); border: 4px solid var(--dark); border-radius: 46px 46px 0 0; box-shadow: inset 0 0 0 6px #b8862e;}
.bench {position: absolute; left: 50%; bottom: 210px; width: 34%; min-width: 300px; height: 140px; transform: translateX(-50%); z-index: 4; background: linear-gradient(180deg, #d39a5f 0 14px, #9a6232 14px 22px, #bf8148 22px 100%); border: 4px solid var(--dark);}
.bench::before {content: ""; position: absolute; left: 16px; right: 16px; top: 34px; bottom: 14px; border: 4px solid #9a6232; box-shadow: inset 0 0 0 4px #c98d55;}
.seal {position: absolute; left: 50%; top: 42px; width: 56px; height: 56px; transform: translateX(-50%); display: flex; align-items: center; justify-content: center; font-size: 1.7rem; z-index: 1; background: #f2c14e; border: 4px solid var(--dark); border-radius: 50%; box-shadow: inset 0 0 0 5px #c98a2e;}
.bench .plate {top: auto; bottom: 10px;}
.dais {position: absolute; left: 50%; bottom: 190px; width: 44%; min-width: 380px; height: 24px; transform: translateX(-50%); z-index: 4; background: linear-gradient(180deg, #d9a96f 0 10px, #a8743f 10px 13px, #c99360 13px 100%); border: 4px solid var(--dark);}
/* empty witness stands beside the bench */
.witness {position: absolute; bottom: 214px; width: 92px; height: 96px; transform: translateX(-50%); z-index: 2;}
.witness .w-rail {position: absolute; left: 0; right: 0; top: 0; height: 10px; background: #9a6232; border: 3px solid var(--dark);}
.witness .w-posts {position: absolute; left: 6px; right: 6px; top: 10px; height: 26px;
  background: repeating-linear-gradient(90deg, #a8693a 0 8px, transparent 8px 18px);}
.witness .w-box {position: absolute; left: 0; right: 0; bottom: 0; height: 60px; background: linear-gradient(180deg, #c98d55 0 8px, #b87a44 8px); border: 4px solid var(--dark);}
.witness .w-box::after {content: ""; position: absolute; left: 10px; right: 10px; top: 14px; bottom: 10px; border: 3px solid #9a6232;}
.witness .w-mic {position: absolute; right: 16px; top: -22px; width: 4px; height: 24px; background: var(--dark);}
.witness .w-mic::before {content: ""; position: absolute; left: -4px; top: -10px; width: 12px; height: 12px; background: #3a3a48; border: 2px solid var(--dark); border-radius: 50%;}
.witness .plate {top: 50px; font-size: .38rem; z-index: 3;}
/* jury box with ever-bobbing pixel jurors */
.jury {position: absolute; right: 1%; bottom: 196px; width: 206px; height: 170px; z-index: 2;}
.juror {position: absolute; image-rendering: pixelated; animation: juror-bob 1.1s steps(2) infinite;}
@keyframes juror-bob {0%, 100% {transform: translateY(0);} 50% {transform: translateY(-5px);}}
.jury .j-back {position: absolute; left: 0; right: 0; bottom: 56px; height: 58px; background: linear-gradient(180deg, #b87a44 0 8px, #9a6232 8px); border: 4px solid var(--dark);}
.jury .j-front {position: absolute; left: -6px; right: -6px; bottom: 0; height: 56px; z-index: 3; background: linear-gradient(180deg, #d39a5f 0 10px, #9a6232 10px 14px, #bf8148 14px); border: 4px solid var(--dark);}
.jury .j-front::after {content: ""; position: absolute; left: 10px; right: 10px; top: 20px; bottom: 8px; border: 3px solid #9a6232;}
.jury .plate {top: auto; bottom: 14px; z-index: 4;}
/* counsel tables closest to you: the speaker stands up into the light */
.table-station {z-index: 6;}
.table-station .who {bottom: 10px;}
.table-station.active .who {bottom: 84px; animation: stand-up .35s steps(4) both, talk .8s steps(2) .35s infinite;}
@keyframes stand-up {from {bottom: 10px;} to {bottom: 84px;}}
.counsel-table {position: absolute; left: 50%; bottom: 14px; width: 250px; height: 96px; transform: translateX(-50%); z-index: 2;
  background: linear-gradient(180deg, #c98d55 0 16px, #8a5329 16px 22px, #a8693a 22px 100%); border: 4px solid var(--dark);
  box-shadow: inset 12px 0 0 rgba(255,255,255,.07), inset -12px 0 0 rgba(0,0,0,.12);}
.counsel-table::before, .counsel-table::after {content: ""; position: absolute; bottom: -14px; width: 14px; height: 14px; background: #6e4020; border: 3px solid var(--dark); border-top: none;}
.counsel-table::before {left: 16px;} .counsel-table::after {right: 16px;}
.counsel-table .papers {position: absolute; top: -8px; width: 36px; height: 10px; background: #fffaf0; border: 2px solid var(--dark);}
.counsel-table .plate {top: 36px;}
.counsel-table .plate b {display: block; font-size: .55rem; margin-bottom: .2rem;}
/* ---------- unlockable courtroom themes ---------- */
.court.dorm {--wall1: #efe6f7; --wall2: #e2d5f0; --wain1: #a58bc4; --wain2: #c1abdb; --trim: #6d5791; --base: #6d5791;
  --tile1: #8fc7c4; --tile2: #7fb9b6; --floor-bg: #8fc7c4; --runner1: #f2a3b8; --runner2: #e891a8; --runner-edge: #fff;}
.court.dorm .pillar {display: none;}
.court.dorm .motto::after {content: " ♪";}
.court.dining {--wall1: #eef7ef; --wall2: #dcefe0; --wain1: #4f9a6a; --wain2: #6bb585; --trim: #2f6a45; --base: #2f6a45;
  --tile1: #fbfbf6; --tile2: #d9534f; --floor-bg: #fbfbf6; --runner1: #f2c14e; --runner2: #e2b04a; --runner-edge: #2f6a45;}
.court.dining .pillar {background: repeating-linear-gradient(90deg, #f3f3ea 0 4px, #ffffff 4px 10px);}
.court.library {--wall1: #e5eedb; --wall2: #d6e3c8; --trim: #4a2e18; --base: #4a2e18;
  --wain1: #4a2e18; --wain2: #7a4a24; --tile1: #8a5a2e; --tile2: #7a4a24; --floor-bg: #8a5a2e;
  --runner1: #2f5e8a; --runner2: #284f75; --runner-edge: #e2b04a;}
.shelves {display: none;}
.court.library .shelves {display: block; position: absolute; left: 0; right: 0; top: 226px; height: 78px;
  background: repeating-linear-gradient(90deg, #b23a3a 0 12px, #2f6fca 12px 22px, #3f8a3a 22px 34px, #e2b04a 34px 42px, #8a3fae 42px 54px, #4a2e18 54px 58px);
  border-top: 6px solid #4a2e18; border-bottom: 6px solid #4a2e18;}
.court.library .pillar {background: repeating-linear-gradient(90deg, #6e4020 0 4px, #8a5329 4px 10px); border-color: #4a2e18;}
/* ---------- typewriter dialogue box ---------- */
.vn-box {position: relative; margin: 1.8rem 0 1.1rem; padding: 1.7rem 1.4rem 1.6rem; background: rgba(24, 20, 40, .96); border: 4px solid #fff; outline: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark);}
.vn-name {position: absolute; top: -1.35rem; left: 1rem; padding: .5rem .8rem; font: .62rem 'Press Start 2P', monospace; color: #fff; background: var(--tag, var(--gold)); border: 4px solid #fff; outline: 4px solid var(--dark);}
.stApp .vn-text {font: 1.6rem/1.3 'VT323', monospace; color: #f6f1e4;}
.tw {opacity: 0; animation: tw-in .01s linear forwards;}
@keyframes tw-in {to {opacity: 1;}}
.vn-next {position: absolute; right: 1rem; bottom: .5rem; color: #f2c14e; font-size: 1rem; opacity: 0; animation: tw-in .01s linear forwards, blink 1s steps(2) infinite;}
@keyframes blink {50% {opacity: 0;}}
/* ---------- investigation board ---------- */
.caseboard {background:#fff8e8;border:4px solid var(--dark);box-shadow:6px 6px 0 var(--dark);padding:1rem;margin:.8rem 0 1.2rem;}
.caseboard-title {font:.66rem/1.8 'Press Start 2P',monospace;color:var(--brown);margin-bottom:.7rem;}
.caseboard-grid {display:grid;grid-template-columns:1fr 1fr;gap:.7rem;}
.caseboard-item {background:#fffdf7;border:3px solid var(--line);padding:.8rem;min-width:0;}
.caseboard-label {font:.5rem/1.7 'Press Start 2P',monospace;color:var(--brown);margin-bottom:.5rem;}
.stApp .caseboard-copy {font:1.25rem/1.25 'VT323',monospace;color:var(--ink);overflow-wrap:anywhere;}
.caseboard-warning {margin-top:.7rem;background:#f7e6b8;border:3px dashed var(--gold);padding:.65rem .8rem;font:1.15rem/1.25 'VT323',monospace;color:var(--ink);}
@media(max-width:650px){.caseboard-grid{grid-template-columns:1fr;}}

/* ---------- action-plan cards ---------- */
.evidence {display: flex; gap: .9rem; align-items: flex-start; margin: .6rem 0; padding: .8rem 1rem; background: var(--cream); border: 4px solid var(--line); box-shadow: 5px 5px 0 var(--dark);}
.evidence-tag {flex: none; padding: .45rem .5rem; background: var(--gold); color: #fff; font: .5rem 'Press Start 2P', monospace; border: 3px solid var(--dark);}
.stApp .evidence-text {font: 1.4rem/1.25 'VT323', monospace; color: var(--ink);}
.section-label {font: .6rem 'Press Start 2P', monospace; color: var(--brown); margin: 1.2rem 0 .3rem;}
/* ---------- gavel + VERDICT slam ---------- */
.gavel-scene {position: relative; height: 210px; margin: .2rem 0 1rem; overflow: hidden; background: var(--cream); border: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark); animation: shake .45s steps(6) .5s;}
.gavel {position: absolute; left: calc(50% - 250px); top: 30px; image-rendering: pixelated; transform-origin: 50% 96%; animation: gavel-swing 1s steps(10) both;}
@keyframes gavel-swing {0% {transform: rotate(-40deg);} 45% {transform: rotate(-55deg);} 60% {transform: rotate(78deg);} 70% {transform: rotate(66deg);} 80%, 100% {transform: rotate(74deg);}}
.sound-block {position: absolute; left: calc(50% - 190px); bottom: 14px; width: 120px; height: 34px; background: linear-gradient(180deg, #c98d55 0 10px, #9a6232 10px); border: 4px solid var(--dark);}
.impact {position: absolute; left: calc(50% - 150px); bottom: 58px; font: 1.2rem 'Press Start 2P', monospace; color: var(--gold); opacity: 0; animation: pop .5s steps(4) .6s both;}
.gavel-word {position: absolute; right: 6%; top: 50%; transform: translateY(-50%); font: clamp(1.8rem, 6vw, 3.6rem) 'Press Start 2P', monospace; color: var(--red); text-shadow: 5px 5px 0 var(--dark); animation: slam .4s steps(5) .6s both;}
@keyframes slam {from {transform: translateY(-50%) scale(3); opacity: 0;} to {transform: translateY(-50%) scale(1); opacity: 1;}}
@keyframes pop {0% {opacity: 0; transform: scale(.4);} 60% {opacity: 1; transform: scale(1.3);} 100% {opacity: 1; transform: scale(1);}}
@keyframes shake {0%, 100% {transform: translate(0, 0);} 20% {transform: translate(-8px, 4px);} 40% {transform: translate(7px, -5px);} 60% {transform: translate(-6px, -3px);} 80% {transform: translate(5px, 4px);}}
/* ---------- verdict stamp ---------- */
.verdict {text-align: center; padding: 1.2rem 1rem; margin: 1.4rem 0 1rem; background: var(--cream); border: 6px double var(--gold); box-shadow: 8px 8px 0 var(--dark); animation: stamp .45s steps(5) 1.1s both;}
.verdict.fail {border-color: var(--red);}
.verdict-word {font: clamp(1.3rem, 4vw, 2.3rem) 'Press Start 2P', monospace; color: #3f8a3a; text-shadow: 4px 4px 0 var(--dark);}
.verdict.fail .verdict-word {color: var(--red);}
@keyframes stamp {from {transform: scale(1.6); opacity: 0;} to {transform: scale(1); opacity: 1;}}
/* ---------- interjection banners ---------- */
.interjection {position: fixed; inset: 0; z-index: 99999; pointer-events: none; display: flex; align-items: center; animation: ij-life 1.7s steps(1) forwards;}
.interjection::before {content: ""; position: absolute; inset: 0; background: #fff; animation: ij-flash .35s steps(3) forwards;}
@keyframes ij-life {0% {visibility: visible;} 100% {visibility: hidden;}}
@keyframes ij-flash {from {opacity: .85;} to {opacity: 0;}}
.ij-band {position: relative; width: 100%; padding: 1.6rem 0; text-align: center; overflow: hidden;
  background: repeating-linear-gradient(-45deg, rgba(0,0,0,.10) 0 14px, transparent 14px 28px), var(--ij);
  border-top: 8px solid var(--dark); border-bottom: 8px solid var(--dark); animation: ij-band 1.7s steps(10) forwards;}
@keyframes ij-band {0% {transform: scaleY(0);} 10% {transform: scaleY(1.2);} 18%, 82% {transform: scaleY(1); opacity: 1;} 100% {transform: scaleY(0); opacity: 0;}}
.ij-word {display: inline-block; font: clamp(2rem, 8vw, 4.6rem) 'Press Start 2P', monospace; color: #fff; text-shadow: 6px 6px 0 var(--dark), -3px -3px 0 var(--dark); animation: ij-word 1.7s steps(12) forwards;}
@keyframes ij-word {0% {transform: translateX(-120vw);} 14% {transform: translateX(3vw);} 20% {transform: translateX(0);} 26% {transform: translate(-8px, 5px);} 32% {transform: translate(8px, -5px);} 38%, 84% {transform: translate(0, 0);} 100% {transform: translateX(120vw);}}
.interjection.good {--ij: #3f9a4a;} .interjection.bad {--ij: #c8413f;} .interjection.order {--ij: #c98a2e;}
.stApp:has(.interjection) .court {animation: shake .5s steps(6) .2s;}
/* ---------- title screen ---------- */
.title-screen {
  position: relative; height: 380px; overflow: hidden; margin: .2rem 0 1rem;
  border: 4px solid var(--dark); box-shadow: 8px 8px 0 var(--dark);
  background:
    radial-gradient(ellipse at 50% 115%, rgba(242,193,78,.95) 0, rgba(242,193,78,0) 55%),
    repeating-linear-gradient(90deg, #7a4a24 0 56px, #66391b 56px 60px);
}
.title-screen::before {content: ""; position: absolute; left: 0; right: 0; top: 0; height: 26px; background: repeating-linear-gradient(90deg, #4a2e18 0 10px, #6e4020 10px 70px); border-bottom: 5px solid var(--dark); z-index: 1;}
.title-sprite {position: absolute; left: 50%; bottom: -40px; transform: translateX(-50%); image-rendering: pixelated; animation: title-bob 1.4s steps(2) infinite;}
@keyframes title-bob {0%, 100% {transform: translate(-50%, 0);} 50% {transform: translate(-50%, -6px);}}
.title-text {position: absolute; inset: 26px 0 0 0; z-index: 2; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;}
.title-kicker {font: .6rem 'Press Start 2P', monospace; color: #fff3c4; letter-spacing: .2em; text-shadow: 3px 3px 0 var(--dark); margin-bottom: 1rem;}
.title-name {font: clamp(2.4rem, 9vw, 5rem)/1.15 'Press Start 2P', monospace; color: #fff;
  text-shadow: 6px 6px 0 var(--red), 10px 10px 0 var(--dark), -3px -3px 0 var(--dark), 3px -3px 0 var(--dark), -3px 3px 0 var(--dark);
  animation: title-drop .6s steps(6) both;}
@keyframes title-drop {from {transform: translateY(-140px); opacity: 0;} to {transform: translateY(0); opacity: 1;}}
.title-sub {margin-top: 1rem; padding: .45rem .7rem; font: .55rem 'Press Start 2P', monospace; color: var(--dark); background: #f2d48a; border: 3px solid var(--dark);}
.title-press {position: absolute; left: 50%; bottom: 16px; transform: translateX(-50%); z-index: 2; white-space: nowrap; padding: .55rem .8rem;
  font: .55rem 'Press Start 2P', monospace; color: #f2c14e; background: var(--dark); border: 3px solid #f2c14e; animation: blink 1.1s steps(2) infinite;}
.versus {text-align: center; font: .7rem 'Press Start 2P', monospace; color: var(--brown); margin: .2rem 0 .6rem;}
/* ---------- loading screen ---------- */
/* Full-screen takeover: covers the whole window, then vanishes when the next screen loads */
.loading {
  position: fixed; inset: 0; z-index: 99990;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  text-align: center; padding: 2rem 1rem;
  background-color: #f4ecdc;
  background-image:
    linear-gradient(rgba(107,58,22,.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(107,58,22,.06) 1px, transparent 1px);
  background-size: 8px 8px;
  border: 12px solid var(--dark); box-shadow: inset 0 0 0 8px var(--gold);
  animation: loading-in .25s steps(3) both;
}
@keyframes loading-in {from {opacity: 0;} to {opacity: 1;}}
.loading .who {width: 160px; height: auto;}
.loading-title {font-size: clamp(.8rem, 2.4vw, 1.3rem) !important;}
.loading .who {image-rendering: pixelated; animation: bob .6s steps(2) infinite;}
.stApp:has(.loading) header {visibility: hidden;}
@keyframes bob {50% {transform: translateY(-6px);}}
.loading-title {font: .9rem 'Press Start 2P', monospace; color: var(--brown); margin: 1.2rem 0 .4rem;}
.dots::after {content: ""; animation: dots 1.2s steps(1) infinite;}
@keyframes dots {0% {content: "";} 25% {content: ".";} 50% {content: "..";} 75% {content: "...";}}
.loading-bar {width: min(420px, 85%); height: 28px; margin: 1.2rem auto .9rem; border: 4px solid var(--dark); background: #efe3c9; overflow: hidden;}
.loading-fill {height: 100%; width: 0; background: repeating-linear-gradient(90deg, var(--gold) 0 18px, #e0a84a 18px 22px); animation: fill 15s steps(30) forwards;}
@keyframes fill {to {width: 95%;}}
.stApp .loading-tip {font: 1.4rem 'VT323', monospace; color: #7a5a3a;}
/* ---------- achievements ---------- */
.reward {display: flex; gap: .9rem; align-items: center; margin: .7rem 0; padding: .8rem 1rem; background: #fff6d6; border: 4px solid var(--gold); box-shadow: 5px 5px 0 var(--dark); animation: stamp .4s steps(4) 1.5s both;}
.reward-icon {font-size: 2rem;}
.reward-kicker {font: .5rem 'Press Start 2P', monospace; color: var(--gold);}
.reward-name {font: .7rem/1.7 'Press Start 2P', monospace; color: var(--brown);}
.stApp .reward-desc {font: 1.2rem 'VT323', monospace; color: var(--ink);}
.trophies {display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: .6rem;}
.trophy {padding: .6rem .7rem; background: var(--cream); border: 3px solid var(--line);}
.trophy.locked {opacity: .45; filter: grayscale(1);}
.trophy b {font: .5rem/1.8 'Press Start 2P', monospace; color: var(--brown);}
.stApp .trophy span {font: 1.1rem 'VT323', monospace;}
/* ---------- widgets ---------- */
.stButton>button {background: var(--red) !important; color: #fff !important; border: 4px solid var(--dark) !important; border-radius: 0 !important; box-shadow: inset -4px -4px 0 #8f2835, inset 4px 4px 0 #ff8a8f, 4px 4px 0 var(--dark) !important; min-height: 3rem; transition: none !important;}
.stButton>button p {font-family: 'Press Start 2P', monospace !important; font-size: .62rem !important; line-height: 1.6 !important; color: #fff !important;}
.stButton>button:hover {filter: brightness(1.1);}
.stButton>button:active {transform: translate(4px, 4px); box-shadow: inset -4px -4px 0 #8f2835 !important;}
.stButton>button:disabled {background: #cdbb9c !important; box-shadow: 4px 4px 0 var(--dark) !important;}
.stTextInput input, .stTextArea textarea {background: #fffdf7 !important; color: var(--dark) !important; border: 4px solid var(--line) !important; border-radius: 0 !important; font: 1.35rem 'VT323', monospace !important;}
.stTextInput input:focus, .stTextArea textarea:focus {border-color: var(--gold) !important;}
div[data-testid="stAudio"] {position: absolute !important; width: 1px !important; height: 1px !important; overflow: hidden !important; opacity: 0 !important;}
.small-note {color: #8a7356 !important; font: 1.1rem 'VT323', monospace !important;}
hr {border-color: var(--line) !important;}
@media (max-width: 760px) {
  .court {height: 440px;}
  .station {transform: translateX(-50%) scale(.62); transform-origin: bottom center;}
  .bench, .dais {transform: translateX(-50%) scale(.7); transform-origin: bottom center;}
  .jury {transform: scale(.7); transform-origin: bottom right;}
  .witness {transform: translateX(-50%) scale(.7); transform-origin: bottom center;}
  .chair, .clock, .motto {display: none;}
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
    # The gavel for the verdict
    "gavel": {
        "grid": [
            "..kkkkkkkkkk..",
            ".kGbbbbbbbbGk.",
            ".kGbbbbbbbbGk.",
            ".kGbbbbbbbbGk.",
            ".kGbbbbbbbbGk.",
            "..kkkkkkkkkk..",
            "......kk......",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kHHk.....",
            ".....kkkk.....",
        ],
        "palette": {"k": "#05060c", "b": "#7a4a24", "G": "#f2c14e", "H": "#a8743f"},
    },
}


# ---------- jurors: one small template, six different looks ----------
JUROR_GRID = [
    "..kkkkkk..",
    ".khhhhhhk.",
    "khhhhhhhhk",
    "khsssssshk",
    "ksessssesk",
    "kssssssssk",
    "ksssmmsssk",
    ".kssssssk.",
    "..kkkkkk..",
    ".kcccccck.",
    "kcccwwccck",
    "kcccccccck",
]
JUROR_LOOKS = [  # (hair, skin, shirt)
    ("#2b2238", "#f1c7a0", "#c8413f"), ("#d9772b", "#f6d2ae", "#2f6fca"), ("#8a8f99", "#e0b48c", "#3f8a3a"),
    ("#f2d48a", "#f6d2ae", "#8a3fae"), ("#4a2e18", "#a8714a", "#e2b04a"), ("#1b1630", "#7a4a2e", "#2f9e98"),
]
for _i, (_hair, _skin, _shirt) in enumerate(JUROR_LOOKS):
    SPRITES[f"juror{_i}"] = {"grid": JUROR_GRID, "palette": {
        "k": "#05060c", "h": _hair, "s": _skin, "e": "#05060c", "m": "#7a3a2a", "c": _shirt, "w": "#f4f1e8"}}


# ---------- facial expressions: small pixel edits on top of each face ----------
#  (row, column, new pixel). "~" is a sweat drop, "x" is a red warning light.
MOOD_EDITS = {
    ("prosecutor", "confident"): [(3, 5, "k"), (3, 6, "k"), (3, 9, "k"), (3, 10, "k"), (7, 7, "s"), (7, 9, "k")],
    ("prosecutor", "nervous"): [(5, 11, "~"), (6, 11, "~"), (7, 6, "k"), (7, 7, "s"), (7, 8, "k"), (7, 9, "s")],
    ("defense", "confident"): [(5, 5, "k"), (5, 10, "k"), (8, 4, "k"), (8, 11, "k")],
    ("defense", "nervous"): [(8, 5, "s"), (8, 10, "s"), (5, 11, "~"), (6, 11, "~")],
    ("judge", "confident"): [(7, 6, "v"), (7, 9, "v"), (6, 6, "a"), (6, 9, "a"),
                             (7, 5, "a"), (7, 7, "a"), (7, 8, "a"), (7, 10, "a")],
    ("judge", "nervous"): [(7, 6, "x"), (7, 9, "x"), (1, 7, "x"), (1, 8, "x")],
}
MOOD_COLORS = {"~": "#7fc8ff", "x": "#ff5c5c"}

# ---------- unlockable outfits: color swaps for the lawyers ----------
OUTFIT_PALETTES = {
    "formal": {
        "prosecutor": {"c": "#2b2b3a", "C": "#1a1a26", "t": "#c9a227"},
        "defense": {"d": "#24365e", "D": "#18243f", "P": "#18243f", "b": "#3a3a48", "B": "#24242e"},
    },
    "party": {
        "prosecutor": {"c": "#ff6fb5", "C": "#c94a8a", "t": "#ffe14a"},
        "defense": {"d": "#ffb03a", "D": "#d9861c", "P": "#d9861c", "b": "#7a5cff", "B": "#5a3fd6"},
    },
}


@st.cache_data
def sprite_uri(name, mood="normal", outfit="classic"):
    """Turn a character grid (plus mood and outfit tweaks) into a crisp SVG data URI."""
    grid = [list(row) for row in SPRITES[name]["grid"]]
    for r, c, ch in MOOD_EDITS.get((name, mood), []):
        grid[r][c] = ch
    palette = {**SPRITES[name]["palette"], **MOOD_COLORS, **OUTFIT_PALETTES.get(outfit, {}).get(name, {})}
    rects = []
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            if ch != ".":
                rects.append(f'<rect x="{x}" y="{y}" width="1.02" height="1.02" fill="{palette[ch]}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {len(grid[0])} {len(grid)}" '
           f'shape-rendering="crispEdges">{"".join(rects)}</svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def sprite_tag(name, scale=9, mood="normal", outfit="classic", cls="who"):
    grid = SPRITES[name]["grid"]
    return (f'<img class="{cls}" src="{sprite_uri(name, mood, outfit)}" width="{len(grid[0]) * scale}" '
            f'height="{len(grid) * scale}" alt="{name}">')


def named(text):
    """Swap "Person A" / "Person B" in AI text for the players' real names."""
    a = st.session_state.get("name_a") or "Person A"
    b = st.session_state.get("name_b") or "Person B"
    for label, name in (("Person A", a), ("person A", a), ("Person B", b), ("person B", b)):
        text = str(text).replace(label, name)
    return text


def esc(text):
    """Escape user / AI text so it can't break the HTML layout."""
    return html.escape(str(text)).replace("\n", "<br>")


CAST = {
    "def":   {"sprite": "defense",    "name": "RORY FINCH", "role": "DEFENSE",     "color": "#2f6fca"},
    "pros":  {"sprite": "prosecutor", "name": "ADA QUILL",  "role": "PROSECUTION", "color": "#8a3fae"},
    "judge": {"sprite": "judge",      "name": "JUDGE AI-9", "role": "THE COURT",   "color": "#c9771c"},
}


def courtroom(active=(), moods=None):
    """Draw the whole courtroom. `active` lists who is speaking (they light up and,
    at the tables, stand up); everyone else dims. `moods` maps "pros"/"def"/"judge"
    to "normal", "confident" or "nervous"."""
    active, moods = set(active), moods or {}
    theme = st.session_state.get("theme", "classic")
    outfit = st.session_state.get("outfit", "classic")
    name_a = esc(st.session_state.get("name_a") or "Person A").upper()
    name_b = esc(st.session_state.get("name_b") or "Person B").upper()

    def state(who):
        if not active:
            return ""
        return " active" if who in active else " dim"

    def counsel(who, left, player):
        """A counsel table closest to the viewer, with that side's lawyer behind it."""
        c = CAST[who]
        return (f'<div class="station table-station{state(who)}" style="left:{left}">'
                f'{sprite_tag(c["sprite"], mood=moods.get(who, "normal"), outfit=outfit)}'
                f'<div class="counsel-table"><div class="papers" style="left:30px"></div>'
                f'<div class="papers" style="right:40px; width:28px"></div>'
                f'<div class="plate"><b>{player}</b>{c["name"]} · {c["role"]}</div></div></div>')

    def witness(left):
        return (f'<div class="witness" style="left:{left}"><div class="w-rail"></div><div class="w-posts"></div>'
                '<div class="w-box"></div><div class="w-mic"></div><div class="plate">WITNESS</div></div>')

    # two rows of jurors (back row sits higher), each bobbing on its own beat
    seats = [(18, 100), (82, 100), (146, 100), (-12, 46), (52, 46), (116, 46)]  # back row, then front row
    jurors = "".join(
        f'<div class="juror" style="left:{x + 6}px; bottom:{y}px; animation-delay:-{i * 0.37:.2f}s;'
        f'{" z-index:2;" if y < 60 else ""}">{sprite_tag(f"juror{i}", scale=5, cls="j")}</div>'
        for i, (x, y) in enumerate(seats))
    jury = (f'<div class="jury"><div class="j-back"></div>{jurors}'
            '<div class="j-front"><div class="plate">JURY</div></div></div>')

    j = CAST["judge"]
    room = (
        f'<div class="court {theme}"><div class="floor"><div class="runner"></div></div>'
        '<div class="ceiling"></div><div class="lamp" style="left:20%"></div><div class="lamp" style="left:80%"></div>'
        '<div class="shelves"></div>'
        '<div class="pillar" style="left:22%"></div><div class="pillar" style="left:36%"></div>'
        '<div class="pillar" style="left:64%"></div><div class="pillar" style="left:78%"></div>'
        '<div class="arch"></div><div class="clock"></div><div class="motto">BE FAIR<br>BE KIND</div>'
        # back of the room: judge in the middle, empty witness stands either side, jury on the right
        f'<div class="station judge-station{state("judge")}" style="left:50%; width:280px">'
        f'<div class="chair"></div>{sprite_tag(j["sprite"], scale=8, mood=moods.get("judge", "normal"))}</div>'
        f'<div class="dais"></div><div class="bench"><div class="seal">⚖</div>'
        f'<div class="plate">{j["name"]}</div></div>'
        + witness("29%") + witness("71%") + jury
        # front of the room, closest to you: Person A's table left, Person B's table right
        + counsel("pros", "19%", "🟪 " + name_a)
        + counsel("def", "81%", "🟦 " + name_b)
        + '</div>'
    )
    st.markdown(room, unsafe_allow_html=True)


def typewriter(text, max_seconds=6.0):
    """Wrap every letter in a span that fades in a little after the one before it."""
    chars = list(str(text))
    step = min(0.035, max_seconds / max(len(chars), 1))
    spans = []
    for i, ch in enumerate(chars):
        if ch == "\n":
            spans.append("<br>")
        else:
            spans.append(f'<span class="tw" style="animation-delay:{i * step:.2f}s">{html.escape(ch)}</span>')
    return "".join(spans), len(chars) * step


def dialogue(who, text):
    c = CAST[who]
    body, finish = typewriter(text)
    st.markdown(
        f'<div class="vn-box" style="--tag:{c["color"]}">'
        f'<div class="vn-name">{c["name"]} · {c["role"]}</div>'
        f'<div class="vn-text">{body}</div>'
        f'<div class="vn-next" style="animation-delay:{finish:.2f}s, {finish:.2f}s">▼</div></div>',
        unsafe_allow_html=True,
    )


def interjection(word):
    """Full-screen pixel banner that flashes across the screen, shakes the court, then disappears."""
    kind = {"SUSTAINED!": "good", "OVERRULED!": "bad"}.get(word, "order")
    st.markdown(f'<div class="interjection {kind}"><div class="ij-band"><div class="ij-word">{word}</div></div></div>',
                unsafe_allow_html=True)


def gavel_verdict():
    """The gavel swings down onto the sound block and VERDICT slams in."""
    st.markdown(
        f'<div class="gavel-scene">{sprite_tag("gavel", scale=8, cls="gavel")}'
        '<div class="sound-block"></div><div class="impact">✦ ✦</div>'
        '<div class="gavel-word">VERDICT!</div></div>',
        unsafe_allow_html=True,
    )


def play_music(track):
    """Loop a track from the assets folder. The player itself is hidden by CSS."""
    path = os.path.join(MUSIC_DIR, track)
    if not os.path.exists(path):
        st.caption(f"🎵 Put {track} in the assets folder to hear music.")
        return
    with open(path, "rb") as file:
        data = file.read()
    try:
        st.audio(data, format="audio/wav", loop=True, autoplay=True)
    except TypeError:  # older Streamlit without loop/autoplay
        st.audio(data, format="audio/wav")


def investigation_board(case):
    """Show attributed testimony, not AI-invented evidence or verified facts."""
    a = esc(st.session_state.get("name_a") or "Person A")
    b = esc(st.session_state.get("name_b") or "Person B")
    claim_a = esc(case.get("person_a", ""))
    claim_b = esc(case.get("person_b", ""))
    st.markdown(
        '<div class="caseboard"><div class="caseboard-title">🔎 CASE INVESTIGATION BOARD</div>'
        '<div class="caseboard-grid">'
        f'<div class="caseboard-item"><div class="caseboard-label">EXHIBIT A · {a}</div>'
        f'<div class="caseboard-copy">{claim_a}</div></div>'
        f'<div class="caseboard-item"><div class="caseboard-label">EXHIBIT B · {b}</div>'
        f'<div class="caseboard-copy">{claim_b}</div></div></div>'
        '<div class="caseboard-warning">⚠ UNVERIFIED TESTIMONY: These are the parties’ accounts, '
        'not independently verified evidence. The court must not invent missing facts.</div></div>',
        unsafe_allow_html=True,
    )


def evidence_cards(plan):
    for index, step in enumerate(plan, 1):
        st.markdown(
            f'<div class="evidence"><div class="evidence-tag">#{index:02d}</div>'
            f'<div class="evidence-text">{esc(named(step))}</div></div>',
            unsafe_allow_html=True,
        )

import hashlib

def jury_votes(resolution, action_plan):
    """Generate repeatable simulated jury votes for a case."""
    content = str(resolution) + "|" + str(action_plan)
    seed = hashlib.sha256(content.encode("utf-8")).digest()

    # Four jurors approve, two dissent.
    # Their positions vary by case, not randomly on reruns.
    dissenters = {seed[0] % 6}
    dissenters.add((seed[0] % 6 + 1 + seed[1] % 5) % 6)

    return [i not in dissenters for i in range(6)]

def show_jury_deliberation(resolution, action_plan):
    votes = jury_votes(resolution, action_plan)
    approved = sum(votes)

    st.markdown("### ⚖️ JURY DELIBERATION")
    st.caption("Six simulated jurors review the court's proposed resolution.")

    columns = st.columns(6)

    for i, (column, approved_vote) in enumerate(zip(columns, votes)):
        with column:
            st.markdown(f"**Juror {i + 1}**")
            st.markdown("🟩 FAIR" if approved_vote else "🟥 DISAGREE")

    st.markdown(
    f"""
    <div style="
        background-color: #173b2e;
        color: #fff4d6;
        padding: 18px;
        border: 3px solid #c69c55;
        font-weight: bold;
        text-align: center;
        font-size: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    ">
        ⚖️ JURY VERDICT: {approved}–{6 - approved} — MAJORITY APPROVES
    </div>
    """,
    unsafe_allow_html=True
)

def reward_cards(new_achievements, new_unlocks):
    for key in new_achievements:
        a = ACHIEVEMENTS[key]
        st.markdown(
            f'<div class="reward"><div class="reward-icon">{a["icon"]}</div><div>'
            f'<div class="reward-kicker">🏆 ACHIEVEMENT UNLOCKED</div>'
            f'<div class="reward-name">{a["name"]}</div><div class="reward-desc">{a["desc"]}</div></div></div>',
            unsafe_allow_html=True,
        )
    for name in new_unlocks:
        st.markdown(
            f'<div class="reward"><div class="reward-icon">🎁</div><div>'
            f'<div class="reward-kicker">NEW UNLOCK</div><div class="reward-name">{esc(name)}</div>'
            f'<div class="reward-desc">Pick it on the opening screen next trial.</div></div></div>',
            unsafe_allow_html=True,
        )


def trophy_case(progress):
    earned = set(progress["achievements"])
    with st.expander(f"🏆 Trophy case · {len(earned)}/{len(ACHIEVEMENTS)} · {progress['settled']} cases settled"):
        cards = "".join(
            f'<div class="trophy{"" if key in earned else " locked"}">{a["icon"]} <b>{a["name"]}</b><br>'
            f'<span>{a["desc"]}</span></div>'
            for key, a in ACHIEVEMENTS.items()
        )
        st.markdown(f'<div class="trophies">{cards}</div>', unsafe_allow_html=True)


def tracker(stage):
    steps = [("PROSECUTION", "1 PROSECUTE"), ("DEFENSE", "2 DEFEND"),
             ("RESOLUTION", "3 RULING"), ("AGREEMENT", "4 AGREE"), ("VERDICT", "5 VERDICT")]
    now = [key for key, _ in steps].index(stage)
    pips = "".join(
        f'<div class="pip {"now" if i == now else "done" if i < now else ""}">{label}</div>'
        for i, (_, label) in enumerate(steps)
    )
    st.markdown(f'<div class="tracker">{pips}</div>', unsafe_allow_html=True)


def press_start():
    """PRESS START: save the two names and go to the case form."""
    a = st.session_state.get("in_name_a", "").strip()
    b = st.session_state.get("in_name_b", "").strip()
    if not a or not b:
        st.session_state.menu_error = "Both players need a name to enter the court."
    elif a.lower() == b.lower():
        st.session_state.menu_error = "The two players need different names."
    else:
        st.session_state.name_a, st.session_state.name_b = a, b
        st.session_state.names_set = True
        st.session_state.flash = "ORDER!"


def go_to_menu():
    """Back to the title screen, with the current names filled in."""
    st.session_state.names_set = False
    st.session_state.in_name_a = st.session_state.get("name_a", "")
    st.session_state.in_name_b = st.session_state.get("name_b", "")


def title_screen():
    """The game's title menu: logo over a big pixel judge, then the players' names."""
    st.markdown(
        f'<div class="title-screen">{sprite_tag("judge", scale=20, cls="title-sprite")}'
        '<div class="title-text"><div class="title-kicker">★ THE PEOPLE\'S COURT PRESENTS ★</div>'
        '<div class="title-name">COURT<br>OF AI</div>'
        '<div class="title-sub">A RETRO COURTROOM GAME</div></div>'
        '<div class="title-press">▼ ENTER THE PLAYERS ▼</div></div>',
        unsafe_allow_html=True,
    )
    if st.session_state.get("menu_error"):
        st.error(st.session_state.pop("menu_error"))
    a_col, b_col = st.columns(2)  # A on the left (Prosecution), B on the right (Defense)
    with b_col:
        st.text_input("🟦 Player B name (defended by Rory Finch)", key="in_name_b", max_chars=16,
                    placeholder="e.g. Jordan")
    with a_col:
        st.text_input("🟪 Player A name (represented by Ada Quill)", key="in_name_a", max_chars=16,
                    placeholder="e.g. Sam")
    st.button("▶ PRESS START", key="press_start", use_container_width=True, on_click=press_start)
    st.markdown('<p class="small-note">Player A brings the complaint. Player B responds to it.</p>',
                unsafe_allow_html=True)


LOADING_TIPS = [
    "The judge is reviewing both statements.",
    "Counsel is shuffling papers dramatically.",
    "Fun fact: Judge AI-9 has never once lost its gavel.",
    "The defense is practicing its serious face.",
    "The prosecution is double-checking every detail.",
    "All rise! (Or stay seated. This is a casual court.)",
    "Settle cases to unlock new courtrooms and outfits.",
]


def loading_screen(title="COURT IS NOW IN SESSION"):
    """Pixel loading screen shown while the AI prepares the trial."""
    st.markdown(
        f'<div class="loading">{sprite_tag("judge", scale=8)}'
        f'<div class="loading-title">{title}<span class="dots"></span></div>'
        f'<div class="loading-bar"><div class="loading-fill"></div></div>'
        f'<div class="loading-tip">TIP: {random.choice(LOADING_TIPS)}</div></div>',
        unsafe_allow_html=True,
    )


# =====================================================================
#  BACKEND + GAME LOGIC
# =====================================================================
try:
    from court_ai import generate_trial
    BACKEND_AVAILABLE = True
except ImportError:
    generate_trial = None
    BACKEND_AVAILABLE = False

SAMPLE_TITLE = "The Case of the Missing Dining Hall Fries"
SAMPLE_A = "I bought fries and left them on the table for a minute. When I came back, they were gone."
SAMPLE_B = "I thought they were leftovers from the group order. I should have asked first."


def demo_trial(person_a, person_b):
    return {
        "prosecutor": person_a,
        "defense": person_b,
        "resolution": "Person A deserves to have their belongings respected. Person B should acknowledge the mistake and make it right without turning a small disagreement into a bigger conflict.",
        "action_plan": [
            "Person B: Apologize directly to Person A for taking the fries without checking.",
            "Person B: Replace the fries or reimburse Person A for their cost.",
            "Both: Ask before taking food or belongings that may belong to someone else.",
        ],
        "prosecutor_mood": "confident", "defense_mood": "nervous", "judge_mood": "normal",
    }


def mood(key):
    value = (st.session_state.trial or {}).get(key, "normal")
    return value if value in ("normal", "confident", "nervous") else "normal"


def init_state():
    progress = load_progress()
    defaults = {
        "case": None, "stage": "SUBMIT", "trial": None, "round": 1,
        "choices": {"a": None, "b": None}, "demo_mode": not BACKEND_AVAILABLE,
        "in_title": "", "in_claim_a": "", "in_claim_b": "",
        "flash": None, "loading_mode": "new", "verdict_recorded": False, "rewards": ([], []),
        "theme": progress.get("theme", "classic"), "outfit": progress.get("outfit", "classic"),
        "names_set": False, "name_a": "", "name_b": "",
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
    st.session_state.verdict_recorded = False
    st.session_state.in_title = ""
    st.session_state.in_claim_a = ""
    st.session_state.in_claim_b = ""


def make_trial(a, b, demo, previous_resolution=None, appeal_feedback=""):
    if demo:
        return demo_trial(a, b)
    if not BACKEND_AVAILABLE:
        raise RuntimeError("The court_ai.py backend could not be imported. Add court_ai.py to this folder or turn on Demo Mode.")
    # Only pass the appeal info if this court_ai.py knows about it (older versions take just a and b).
    params = inspect.signature(generate_trial).parameters
    if previous_resolution and "previous_resolution" in params and "appeal_feedback" in params:
        return generate_trial(a, b, previous_resolution=previous_resolution, appeal_feedback=appeal_feedback)
    return generate_trial(a, b)


def validate_trial(trial):
    for key in ("prosecutor", "defense", "resolution"):
        if key not in trial or not isinstance(trial[key], str):
            raise ValueError(f"AI backend returned an invalid response: missing {key}.")
    plan = trial.get("action_plan", [])
    if not isinstance(plan, list) or not all(isinstance(item, str) for item in plan):
        raise ValueError("AI backend returned an invalid action plan.")
    return trial


def friendly_error(exc):
    message = str(exc)
    if "11434" in message or "connection" in message.lower() or "refused" in message.lower():
        return "The court cannot reach Ollama. Make sure Ollama is running and the model is installed."
    return f"The court ran into a problem: {message}"


def pick_theme():
    st.session_state.theme = st.session_state.pick_theme


def pick_outfit():
    st.session_state.outfit = st.session_state.pick_outfit


def toggle_music():
    st.session_state.music = st.session_state.music_toggle


def start_trial():
    """Start Trial button: check the statements, then switch to the loading screen."""
    title = st.session_state.in_title.strip()
    a = st.session_state.in_claim_a.strip()
    b = st.session_state.in_claim_b.strip()
    if not a or not b:
        if not a:
            st.error(f"{st.session_state.name_a}'s statement is required.")
        if not b:
            st.error(f"{st.session_state.name_b}'s statement is required.")
        return
    # Remember settings now: these widgets disappear once the trial starts.
    st.session_state.demo_mode = st.session_state.get("use_demo", not BACKEND_AVAILABLE)
    progress = load_progress()
    progress["theme"], progress["outfit"] = st.session_state.theme, st.session_state.outfit
    save_progress(progress)
    st.session_state.case = {"title": title or "Untitled Case", "person_a": a, "person_b": b}
    st.session_state.trial = None
    st.session_state.round = 1
    st.session_state.choices = {"a": None, "b": None}
    st.session_state.verdict_recorded = False
    st.session_state.loading_mode = "new"
    st.session_state.stage = "LOADING"


def retry_resolution():
    """Request revised ruling: remember why it was rejected, then show the loading screen."""
    st.session_state.appeal_text = st.session_state.get("appeal_feedback", "").strip()
    st.session_state.round += 1
    st.session_state.loading_mode = "retry"
    st.session_state.stage = "LOADING"


def generate_case():
    """Runs while the loading screen is showing. Asks the AI for the trial (or a new resolution)."""
    case = st.session_state.case
    retry = st.session_state.loading_mode == "retry"
    try:
        if st.session_state.demo_mode:
            time.sleep(1.5)  # demo mode is instant; pause so the loading screen is visible
        previous = st.session_state.trial["resolution"] if retry else None
        appeal = st.session_state.get("appeal_text", "") if retry else ""
        trial = validate_trial(make_trial(case["person_a"], case["person_b"], st.session_state.demo_mode,
                                          previous_resolution=previous, appeal_feedback=appeal))
    except Exception as exc:
        if retry:
            st.session_state.round -= 1
            st.session_state.stage_error = friendly_error(exc)
            st.session_state.stage = "VERDICT"
            return
        st.session_state.start_error = friendly_error(exc)
        # Go back to the form with the statements still filled in.
        st.session_state.in_title = "" if case["title"] == "Untitled Case" else case["title"]
        st.session_state.in_claim_a = case["person_a"]
        st.session_state.in_claim_b = case["person_b"]
        st.session_state.case = None
        st.session_state.stage = "SUBMIT"
        return

    if retry:  # keep the opening arguments, take the new ruling
        st.session_state.trial["resolution"] = trial["resolution"] + f" (Resolution round {st.session_state.round}.)"
        if trial.get("action_plan"):
            st.session_state.trial["action_plan"] = trial["action_plan"]
        st.session_state.trial["judge_mood"] = trial.get("judge_mood", "normal")
        st.session_state.choices = {"a": None, "b": None}
        st.session_state.verdict_recorded = False
        st.session_state.stage = "RESOLUTION"
    else:
        st.session_state.trial = trial
        st.session_state.stage = "PROSECUTION"
    st.session_state.flash = "ORDER!"


def advance():
    order = ["PROSECUTION", "DEFENSE", "RESOLUTION", "AGREEMENT"]
    current = order.index(st.session_state.stage)
    st.session_state.stage = order[min(current + 1, len(order) - 1)]


def choose(side, value):
    st.session_state.choices[side] = value
    if value == "decline":
        st.session_state.flash = "OVERRULED!"


# =====================================================================
#  SCREENS
# =====================================================================
init_state()

# ---- music toggle (top right) ----
_, music_col = st.columns([3, 1])
with music_col:
    st.toggle("🎵 Music", key="music_toggle", value=st.session_state.get("music", False), on_change=toggle_music)
settled_now = (st.session_state.stage == "VERDICT"
               and all(v == "accept" for v in st.session_state.choices.values()))
if st.session_state.get("music"):
    play_music("settled.wav" if settled_now else "trial.wav")

# ---- title menu: shown until both players enter their names ----
if not st.session_state.names_set:
    title_screen()
    st.stop()

st.markdown(
    '<div class="hero"><div class="hero-kicker">★ THE PEOPLE\'S COURT · EST. 2026 ★</div>'
    '<div class="hero-title">COURT OF AI</div>'
    '<div class="hero-sub">Your side of the story is now in session.</div></div>',
    unsafe_allow_html=True,
)
NAME_A, NAME_B = st.session_state.name_a, st.session_state.name_b
st.markdown(f'<div class ="versus">🟪 {esc(NAME_A).upper()} &nbsp;VS&nbsp; {esc(NAME_B).upper()} 🟦</div>',
            unsafe_allow_html=True)
# ---- interjection banner (plays once) ----
if st.session_state.flash:
    interjection(st.session_state.flash)
    st.session_state.flash = None

if st.session_state.case is None:
    # ---------------- Case submission ----------------
    progress = load_progress()
    if st.session_state.get("start_error"):
        st.error(st.session_state.pop("start_error"))
    st.markdown('<div class="case-strip">CASE FILE 001 · NEW MATTER · AWAITING STATEMENTS</div>', unsafe_allow_html=True)

    # unlockables: only show what this save file has earned
    themes, outfits = unlocked(THEMES, progress), unlocked(OUTFITS, progress)
    if st.session_state.theme not in themes:
        st.session_state.theme = "classic"
    if st.session_state.outfit not in outfits:
        st.session_state.outfit = "classic"
    t_col, o_col = st.columns(2)
    with t_col:
        st.selectbox("🏛️ Courtroom", themes, index=themes.index(st.session_state.theme), key="pick_theme",
                     format_func=lambda k: THEMES[k]["name"], on_change=pick_theme)
    with o_col:
        st.selectbox("👔 Outfits", outfits, index=outfits.index(st.session_state.outfit), key="pick_outfit",
                     format_func=lambda k: OUTFITS[k]["name"], on_change=pick_outfit)
    locked = [f'🔒 {item["name"]} ({item["needs"]} settled)'
              for item in list(THEMES.values()) + list(OUTFITS.values()) if progress["settled"] < item["needs"]]
    if locked:
        st.caption("Locked: " + " · ".join(locked))

    courtroom()
    dialogue("judge", "Order, order! Every great trial starts with two sides. "
             "Present both statements, and this court will hear the arguments, weigh a compromise, "
             "and issue an action plan.")

    st.text_input("Case title (optional)", key="in_title", placeholder="e.g. The Case of the Stolen Snacks")
    right, left = st.columns(2)
    with left:
        st.markdown(f"### 🟦 {esc(NAME_B).upper()}")
        st.text_area(f"What happened from {NAME_B}'s perspective? (represented by the Defense)", key="in_claim_b",
                     height=160, placeholder="Explain your side of the story...")
    with right:
        st.markdown(f"### 🟪 {esc(NAME_A).upper()}")
        st.text_area(f"What happened from {NAME_A}'s perspective? (represented by the Prosecution)", key="in_claim_a",
                     height=160, placeholder="Explain what happened and why you're upset...")
    st.checkbox("Use Demo Mode (no Ollama required)", key="use_demo", value=not BACKEND_AVAILABLE)
    c1, c2 = st.columns(2)
    with c1:
        st.button("Load Sample Case", key="load_sample", use_container_width=True,
                  on_click=lambda: st.session_state.update({
                      "in_title": SAMPLE_TITLE, "in_claim_a": SAMPLE_A, "in_claim_b": SAMPLE_B}))
    with c2:
        st.button("⚖ Start Trial", key="start", use_container_width=True, on_click=start_trial)
    trophy_case(progress)
    st.button("↩ Change players (title menu)", key="to_menu", on_click=go_to_menu)
    st.markdown('<p class="small-note">COURT NOTICE: The AI mediator is not a real judge. '
                'Keep statements respectful and avoid sharing private information.</p>', unsafe_allow_html=True)

else:
    case = st.session_state.case
    stage_name = st.session_state.stage

    if stage_name == "LOADING":
        retrying = st.session_state.loading_mode == "retry"
        loading_screen("THE COURT RECONSIDERS" if retrying else "COURT IS NOW IN SESSION")  # shows while the AI works
        generate_case()
        st.rerun()

    trial = st.session_state.trial
    st.markdown(f'<div class="case-strip">CASE FILE · {esc(case["title"].upper())} · '
                f'ROUND {st.session_state.round}/{MAX_ROUNDS}</div>', unsafe_allow_html=True)
    tracker(stage_name)
    if stage_name in ("PROSECUTION", "DEFENSE", "RESOLUTION"):
        with st.expander("🔎 OPEN CASE INVESTIGATION BOARD", expanded=True):
            investigation_board(case)

    if stage_name == "PROSECUTION":
        courtroom(active=["pros"], moods={"pros": mood("prosecutor_mood")})
        dialogue("pros", f"{st.session_state.name_a} states: {case['person_a']}")
        st.button("Hear the defense ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "DEFENSE":
        courtroom(active=["def"], moods={"def": mood("defense_mood"), "pros": mood("prosecutor_mood")})
        dialogue("def", f"{st.session_state.name_b} states: {case['person_b']}")
        st.button("Approach the bench ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "RESOLUTION":
        courtroom(active=["judge"], moods={"judge": mood("judge_mood")})
        dialogue("judge", named(trial["resolution"]))
        plan = trial.get("action_plan", [])
        if plan:
            st.markdown('<div class="section-label">📜 COURT-ORDERED ACTION PLAN</div>', unsafe_allow_html=True)
            evidence_cards(plan)
        st.button("Proceed to agreement ▶", key="next", on_click=advance, use_container_width=True)

    elif stage_name == "AGREEMENT":
        reaction = {"accept": "confident", "decline": "nervous", None: "normal"}
        courtroom(active=["def", "pros"], moods={"def": reaction[st.session_state.choices["b"]],
                                                 "pros": reaction[st.session_state.choices["a"]]})
        dialogue("judge", "Both parties must now decide: do you accept the proposed resolution? "
                 "The verdict will be revealed once both have answered.")
        a_col, b_col = st.columns(2)  # Person A on the left, Person B on the right (same as their tables)
        for col, side, label in ((a_col, "a", f"🟪 {esc(NAME_A).upper()}"), (b_col, "b", f"🟦 {esc(NAME_B).upper()}")):
            with col:
                st.markdown(f"### {label}")
                locked_in = st.session_state.choices[side] is not None
                st.button("✓ Accept", key=f"accept_{side}", disabled=locked_in, on_click=choose,
                          args=(side, "accept"), use_container_width=True)
                st.button("✕ Decline", key=f"decline_{side}", disabled=locked_in, on_click=choose,
                          args=(side, "decline"), use_container_width=True)
                if locked_in:
                    st.caption(f"Answer recorded: {st.session_state.choices[side].upper()}")
        if all(st.session_state.choices.values()):
            st.button("⚖ Reveal Verdict", key="see_verdict", use_container_width=True,
                      on_click=lambda: st.session_state.update({"stage": "VERDICT"}))

    
    elif stage_name == "VERDICT":
        accepted = all(value == "accept" for value in st.session_state.choices.values())

        if st.session_state.get("stage_error"):
            st.error(st.session_state.pop("stage_error"))

        # Save achievements once per verdict
        if not st.session_state.verdict_recorded:
            progress = load_progress()
            st.session_state.rewards = record_verdict(
                progress,
                case,
                st.session_state.round,
                accepted,
                MAX_ROUNDS
            )
            save_progress(progress)
            st.session_state.verdict_recorded = True

        gavel_verdict()

        if accepted:
            courtroom(
                active=["judge"],
                moods={
                    "judge": "confident",
                    "pros": "confident",
                    "def": "confident"
                }
            )

            dialogue(
                "judge",
                "The parties have accepted the court's resolution. This case is settled!"
            )

            st.markdown(
                '<div class="verdict"><div class="verdict-word">CASE SETTLED</div></div>',
                unsafe_allow_html=True
            )

            reward_cards(*st.session_state.rewards)

            st.markdown(
                '<div class="section-label">📜 FINAL ACTION PLAN</div>',
                unsafe_allow_html=True
            )

            evidence_cards(trial.get("action_plan", []))

        else:
            courtroom(
                active=["judge"],
                moods={
                    "judge": "nervous",
                    "pros": "nervous",
                    "def": "nervous"
                }
            )

            if st.session_state.round < MAX_ROUNDS:
                dialogue(
                    "judge",
                    "The proposed resolution was not accepted by both parties. "
                    "Very well, the court will attempt another resolution."
                )
            else:
                dialogue(
                    "judge",
                    "The proposed resolution was not accepted by both parties, "
                    "and this court has run out of attempts."
                )

            st.markdown(
                '<div class="verdict fail"><div class="verdict-word">NO DEAL</div></div>',
                unsafe_allow_html=True
            )

            reward_cards(*st.session_state.rewards)

            if st.session_state.round < MAX_ROUNDS:
                st.text_area(
                    "Why was the ruling rejected? (optional)",
                    key="appeal_feedback",
                    placeholder="Explain what the judge got wrong...",
                    height=110
                )

                st.button(
                    "Request revised ruling",
                    key="retry",
                    on_click=retry_resolution,
                    use_container_width=True
                )
            else:
                st.warning(
                    "The court has reached its maximum number of resolution attempts."
                )

        # NEW: Six simulated jurors vote on the proposed resolution
        show_jury_deliberation(
            trial.get("resolution", ""),
            trial.get("action_plan", [])
        )

        st.button(
            "Start a new trial",
            key="reset_verdict",
            on_click=reset_trial,
            use_container_width=True
        )


    st.divider()
    if stage_name != "VERDICT":
        st.button("↺ Abandon case / New trial", key="reset_sidebar", on_click=reset_trial)
    st.markdown('<p class="small-note">COURT OF AI · A fictional mediation experience, not legal advice.</p>',
                unsafe_allow_html=True)