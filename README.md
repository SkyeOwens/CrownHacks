# Court of AI

A retro courtroom game for settling roommate fights, group project drama and every other small conflict that's too awkward to talk about.

Two people each type their side of what happened. A pixel prosecutor and a pixel defense attorney argue the case, a robot judge proposes a fair fix, and both players decide whether to accept it. If one of them says no, they explain why and the judge tries again.

Built for Crown Hacks 2026.

## Why we made it

Most arguments between roommates or friends aren't big. They're about fries, dishes, the thermostat, or a charger that went missing. But they're uncomfortable to bring up, so people avoid them until they turn into something bigger. We wanted to make sitting down and sorting it out feel less like a confrontation and more like a game.

## How it plays

1. **Enter both players' names** on the title screen.
2. **Each player tells their side.** You can also pick one of the sample cases to try it out.
3. **The trial runs.** The prosecutor argues for Player A, the defense argues for Player B, then the judge proposes a resolution and a three-step action plan.
4. **Both players accept or decline.**
   - Both accept: the gavel comes down and you get an official Court Order with both names on it.
   - Someone declines: they say what was unfair and the judge writes a revised ruling. The court gives you three tries.

## Features

- Pixel-art courtroom with a judge's bench, witness stands, a jury box and counsel tables. Whoever is speaking stands up into a spotlight.
- Characters change expressions (normal, confident, nervous) depending on how the case is going.
- Dialogue types out letter by letter.
- ORDER! and OVERRULED! banners, a gavel animation and a verdict stamp.
- Appeals: decline a ruling, explain why, and get a revised one.
- A simulated jury vote on the verdict screen.
- An official Court Order when a case settles, with the action plan and everyone's "signatures".
- Achievements, plus unlockable courtrooms (Dorm Room, Dining Hall, Library) and outfits.
- Two original chiptune tracks, one for the trial and one for when a case settles.
- Runs locally. The AI model runs on your own computer through Ollama, so nobody's drama gets sent to a server.

## Running it

You need Python 3.10 or newer.

```bash
pip install -r requirements.txt
```

For the full AI version, install [Ollama](https://ollama.com) and download the model:

```bash
ollama pull qwen2.5:7b
```

Then start the app from the project folder:

```bash
streamlit run app.py
```

It opens in your browser at `http://localhost:8501`.

**No Ollama?** Tick **Use Demo Mode** on the case screen. Every screen still works; the arguments just come from a built-in example instead of the model. This is also how the online version runs, since Ollama can't run on Streamlit Cloud.

## Project files

| File | What it does |
|---|---|
| `app.py` | The game: screens, courtroom, characters, animations |
| `court_ai.py` | Sends both statements to the local model and checks its answer |
| `court_logic.py` | Achievements, unlockables and the save file |
| `assets/` | `trial.wav` and `settled.wav` music |
| `progress.json` | Your saved achievements (created after your first verdict) |

## Built with

- [Streamlit](https://streamlit.io) for the app
- [Ollama](https://ollama.com) running Qwen 2.5 (7B) locally
- Plain CSS and SVG for all the pixel art. The characters are drawn from text grids in `app.py`, and the music was generated in Python.

## A note

Court of AI is a game, not legal advice or real mediation. If a conflict involves safety, harassment or anything serious, talk to an RA, a counselor or someone you trust.
