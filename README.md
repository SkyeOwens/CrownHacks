Court of AI

Court of AI is a pixel-art courtroom game for settling small, everyday arguments. Two people each explain their side, the case goes to trial, and a judge running on your own computer suggests a fair way to fix it. If someone thinks the ruling is unfair, they can say why and get a new one.

We made this for Crown Hacks 2026.

Why

Most fights between roommates or friends aren't serious. Somebody ate somebody's fries. The dishes have been in the sink for a week. The thermostat keeps getting turned down. Nobody wants to bring it up because it's awkward, so it sits there and gets worse. We wanted to turn that conversation into something closer to a game, so it's easier to actually have it.

How a trial works
Title screen. Both players type their names and press START.
The case. Each player writes what happened from their side. You can give the case a title or leave it blank and the court names it for you (for example, a complaint about loud music becomes "The Midnight Noise Affair"). There are also six sample cases if you just want to try it.
Prosecution and defense. Player A's lawyer, Ada Quill, and Player B's lawyer, Rory Finch, each stand up and read their client's statement. The Case Investigation Board shows both statements side by side and reminds everyone that they're unverified accounts, not proven facts.
The ruling. Judge AI-9 reads both sides and gives a short resolution with a three-step action plan. Every step says who is responsible for it: Player A, Player B or Both.
Accept or decline. Each player chooses.
If both accept, the gavel comes down, the jury reacts, and the court prints an Official Court Order with the plan and both names on it.
If someone declines, they can explain what was wrong with the ruling, and the judge writes a revised one. The court allows three rounds in total.
How the judge decides

The AI part lives in court_ai.py and runs through Ollama on your own machine, so the statements never leave your computer.

Each ruling takes two passes:

Draft. The model writes a ruling following a list of rules we gave it. For example: don't invent facts, don't assume both people are equally at fault, don't make the person who was wronged clean up after the other person, and only suggest fixes that are actually possible.
Review. The model checks its own draft against the original statements, step by step, and replaces any step that doesn't hold up. If the review fails for some reason, the draft is used instead.

There's also a small safety net for food cases. If someone already ate the food, the court won't order them to "return" it. It changes the order to replacing it instead.

The judge's answer is checked before it's shown. It has to include a resolution and exactly three action steps, and each step has to start with "Person A:", "Person B:" or "Both:". The app then swaps in the players' real names.

Other features
The courtroom. Judge's bench in the middle, an empty witness stand on each side, a six-person jury box and two counsel tables up front. Whoever is talking stands up into a spotlight.
Faces. Characters can look normal, confident or nervous depending on the case. At the verdict, each juror smiles or frowns based on a simulated jury vote.
Typewriter dialogue and an ORDER! banner when court is in session.
Music. Two original chiptune loops, one for the trial and one for when a case settles. Turn them on with the Music toggle.
Achievements, like Settled in Round 1, Snack Crimes Specialist and Made It to Round 3. They're saved in progress.json.
Unlockables. New courtrooms (Dorm Room, Dining Hall, Library) and outfits (Formal Night, Party Mode) unlock as you settle more cases.
Demo Mode. Runs the whole game with a built-in example ruling, without Ollama.
