# Flappy Bird

A minimalist implementation of the classic Flappy Bird game written in **Python** using **Pygame**.

The player controls a small circle that jumps with the space bar, avoiding moving pipes.  
The goal is to survive as long as possible and beat your previous top score.

---

## Features
- Smooth jump physics with gravity
- Randomly generated pipes with consistent gaps
- Collision detection for pipes and ground
- Score tracking and persistent high score (`top-score.txt`)
- Minimal graphics for clarity and performance

---

## Requirements
- Python 3.x
- [Pygame](https://www.pygame.org/)

Install dependencies:
```bash
pip install pygame
```

## How to Run
Clone this repository:
```bash
git clone https://github.com/yourusername/flappy-bird-project.git
```

Navigate to the project directory:
```bash
cd flappy-bird-project
```

Ensure `top-score.txt` exists (create it manually if missing):
```bash
echo 0 > top-score.txt
```

Run the game:
```bash
python flappy-bird.py
```

---

## Controls
- **Space** — Jump / Start game
- **Close Window** — Quit game

---

## File Structure
```bash
flappy-bird.py     # Main game script
top-score.txt      # Stores persistent high score
README.md          # Project documentation
```

---

## How It Works
- **Main Loop:** Runs the game and event handling
- **Pipes:** Stored as `[x_position, gap_start, gap_end]` in a list
- **Player Movement:** Controlled by MOMENTUM (jumping) and gravity
- **Collision:** Checks if the player's Y-position is outside the gap while in the pipe’s X-range
- **Scoring:** Increments when the player passes a pipe without collision
- **Game Over:** Displays score and best score; updates `top-score.txt` if needed

---

## License
This project is licensed under the MIT License.  
See the LICENSE file for details.
