# Tron Light Cycle Game

> A real-time, two-player Tron light cycle game built in Python with Pygame — featuring collision detection, persistent trail rendering, score tracking, and a documented debugging journey from broken to fully working.

---

## Table of Contents

- [Analysis & STEM Significance](#-analysis--stem-significance)
- [Technical Depth](#-technical-depth)
- [Installation & Usage](#-installation--usage)
- [Controls](#-controls)
- [Learning Outcomes](#-learning-outcomes)
- [The Bug That Taught Me The Most](#-the-bug-that-taught-me-the-most)

---

## Analysis & STEM Significance

This project is a faithful Python implementation of the classic **Tron light cycle** arcade game. Two players navigate bikes across a grid; each bike leaves a permanent light trail behind it, and the first player to collide with a wall, their own trail, or the opponent's trail loses the round.

From an **A-Level Computer Science** perspective, this project demonstrates:

- **Object-Oriented Design** — the `Player` class encapsulates position, velocity (bearing), colour, and all rendering/movement behaviour, illustrating encapsulation and single-responsibility principles.
- **Real-time event loops** — the main `while` loop runs at a locked **60 FPS** via `clock.tick(60)`, a core concept in game engines and embedded systems.
- **Collision detection** — using Pygame's `Rect.collidelist()` and list-membership testing (`in path`) to detect trail and wall collisions in O(n) time.
- **State machines** — the `new` boolean flag acts as a minimal finite state machine that transitions the game from "playing" → "resetting" → "playing".
- **Debugging & software iteration** — the repo deliberately preserves the original buggy version alongside the fixed version, making the debugging process a first-class artefact.

---

## Technical Depth

### Coordinate System & Vector Motion

Each player stores a `bearing` — a 2-tuple `(dx, dy)` — that acts as a **velocity vector**. On every frame, the player's position updates via:

```python
self.x += self.bearing[0]
self.y += self.bearing[1]
```

A speed of `±2 pixels/frame` at 60 FPS yields a movement rate of **120 pixels per second**. Direction changes are handled by keyboard events that simply swap the bearing tuple — no physics engine required, because Tron's movement is purely discrete and axis-aligned.

### Trail as a Growing List of Rects

The trail is stored as a **list of `(pygame.Rect, player_id)` tuples**. Every frame, the current player rect is appended to `path`. Collision detection is then a membership check:

```python
if (obj.rect, '1') in path or (obj.rect, '2') in path:
    # collision!
```

This is a classic **space-time tradeoff**: storing every past position costs O(n) memory as the game progresses, but makes the collision check a simple linear scan. For a bounded 600×600 grid moving at 2px/frame, the path list reaches at most ~90,000 entries at the extreme — entirely manageable for a real-time game.

### Wall Construction with Offsets

The playing field sits inside a 600×660 window. The `offset = height - width = 60` pixel gap at the top is reserved for the **scoreboard**. The four boundary walls are constructed as `pygame.Rect` objects positioned relative to this offset, ensuring the scoreboard is never overdrawn by gameplay:

```python
wall_rects = [
    pygame.Rect([0, offset, 15, height]),       # Left wall
    pygame.Rect([0, offset, width, 15]),        # Top wall
    pygame.Rect([width - 15, offset, 15, height]),  # Right wall
    pygame.Rect([0, height - 15, width, 15])    # Bottom wall
]
```

### Debounce via `time.time()`

A `check_time` debounce guard prevents a single collision from firing the reset logic multiple times in rapid succession:

```python
if (time.time() - check_time) >= 0.1:
    check_time = time.time()
    # ... award point and reset
```

This is a software **debouncing** pattern — identical to the hardware technique used in microcontroller inputs to filter signal noise.

### The Critical Indentation Bug

The repo includes `buggy code(fixed).py`, which preserves the original broken version. The root cause was a Python indentation error: the score-increment block was placed *outside* the `if (time.time() - check_time) >= 0.1:` guard, meaning points were awarded and the game reset on *every single frame* for the duration of the collision, not just once. The fix was a single level of indentation — a one-character change that completely changed the control flow. This is documented inline in the buggy file with the comment:

```
#IT WAS BUGGY BC THIS WAS NOT IN THE IF STATEMENT
```

---

## Installation & Usage

### Prerequisites

- Python `>=3.10, <3.12`
- [Poetry](https://python-poetry.org/) (recommended) **or** pip

### With Poetry (recommended)

```bash
git clone https://github.com/77natsu77/tron-game.git
cd tron-game
poetry install
poetry run python main.py
```

### With pip

```bash
git clone https://github.com/YOUR_USERNAME/tron-game.git
cd tron-game
pip install pygame==2.5.2
python main.py
```

---

## Controls

| Action | Player 1 (Cyan) | Player 2 (Magenta) |
|---|---|---|
| Move Up | `W` | `↑` |
| Move Down | `S` | `↓` |
| Move Left | `A` | `←` |
| Move Right | `D` | `→` |

Crash into a wall, your own trail, or your opponent's trail and you lose the round. The score persists across rounds until you close the window.

---

## Learning Outcomes

Building this project developed hands-on mastery of:

- **Pygame's game loop architecture** — understanding the render → event → update cycle and why `display.flip()` must come at the end of every frame.
- **OOP in a real application** — using a `Player` class rather than loose variables to keep state clean and reusable (the `new_game()` factory function simply instantiates fresh objects rather than manually resetting a dozen variables).
- **Collision detection without a physics engine** — implementing lightweight AABB (Axis-Aligned Bounding Box) collision via `Rect.collidelist()` and list membership.
- **Debugging methodology** — isolating a bug by comparing expected vs. actual behaviour frame-by-frame, reading the control flow, and identifying that indentation in Python is *semantically meaningful*, not just stylistic.
- **Dependency management** — using `pyproject.toml` and Poetry to pin dependencies (`pygame ^2.5.2`) and declare Python version constraints, mirroring professional project structure.
- **Software archaeology** — preserving the buggy version as a documented learning artefact, demonstrating version history thinking even before using Git branches.

---

## The Bug That Taught Me The Most

The single most educational moment in this project was the indentation bug. In Python, whitespace is syntax. Moving the score/reset block from outside to inside the debounce `if` block changed the program's behaviour from "resets 60 times per second on collision" to "resets exactly once per collision." 

This is a subtle but critical distinction that highlights a key A-Level concept: **control flow** is determined by code structure, not by programmer intent. The fix required no new logic — only correct placement of existing logic.

---

## Repository Structure

```
tron-game/
├── main.py                  # Final, working game
├── buggy code(fixed).py     # Original version with bug annotated
├── pyproject.toml           # Poetry dependency config
├── poetry.lock              # Pinned dependency lockfile
└── README.md
```
