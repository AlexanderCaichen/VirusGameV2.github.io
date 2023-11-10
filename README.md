# VirusGameV2

Web App link: https://alexandercaichen.github.io/root.html

GitHub link: https://github.com/AlexanderCaichen/AlexanderCaichen.github.io

A game that simulates cells mutating to survive a mutating virus infection.

Work in progress.

---

Game can be run locally via:
1. Download repository
2. Start Websocket server via `python handler.py` in terminal within the local project directory.
3. Open `root.html` within the browser of your choice.

One can alternatively after Step 2:
3. Start Python server locally via `python -m http.server` in terminal.
4. Enter `http://localhost:8000/[PATH TO root.html FROM DIRECTORY PREVIOUS COMMAND WAS CALLED]` in browser of your choice.

---

Current content upon starting game:
- 5 tables showing what cells are infected, what viruses exist (infecting or not), and total statistics.
- A timer.
- A pause button.
- A series of buttons that can change contents once you click on one with a mouse then type with a keyboard.

TBA:
- Stop viruses from going extinct within ~60 ticks (probably need to increase cell life)
- Allow changing of own genome (add new cells)
- Settings/New game modes
- A better, more interesting interface
