# Gold Rush Roundup

**Demo Video:** [https://youtu.be/A1yZZR70tK8](https://youtu.be/A1yZZR70tK8)
**Repository:** https://github.com/Awhite1111/gold-rush-roundup

## Description

Gold Rush Roundup is a Wild West themed maze game built entirely in Python using the Pygame library. You play as a cowboy navigating a frontier town maze, collecting gold coins while avoiding outlaw enemies. Grab a Sheriff's Badge to turn the tables and hunt down the outlaws yourself! The game features two progressively harder levels, screen wrapping, a replay system, and a full HUD with score and lives tracking.

This project is relevant to digital arts and media because it combines interactive game design, real-time sprite-based animation, procedural level layout, synthesized audio, and player-driven visual storytelling — all core elements of game art and interactive media.

## Files

- `src/project.py` — The main game source file containing all game logic, drawing functions, sound generation, the Outlaw class, level loop, and the main entry point.
- `requirements.txt` — Lists the third-party libraries needed to run the game: `pygame` and `numpy`.
- `week1_project.py` — Week 1 progress file: basic maze rendering and player movement.
- `week2_project.py` — Week 2 progress file: gold coin collection and outlaw enemies added.
- `week3_project.py` — Week 3 progress file: Sheriff's Badge power-up and HUD added.
- `README.md` — This file. Explains the project, design decisions, and future improvements.

## How to Run

1. Install the requirements:
   ```
   pip install pygame numpy
   ```
2. From the root of the repository, run:
   ```
   python src/project.py
   ```
3. Use **Arrow Keys** to move the cowboy. Press **ESC** to quit at any time. Press **R** to replay or **Q** to quit on the end screen.

## Features

- **Procedurally generated sound effects** — All audio is synthesized at runtime using numpy waveforms (no external audio files). Includes distinct sounds for coin collection, badge pickup, outlaw elimination (gunshot sound), taking a hit, level clear, and game over.
- **Tile-based maze** — A grid-based frontier town layout rendered with Pygame's drawing tools, with wall collision detection using corner-based pixel checking.
- **Screen wrapping** — Walk off the left or right edge of the maze through the tunnel and reappear on the opposite side.
- **Gold coin collection** — Coins fill every open tile. Collecting all coins on a level advances you to the next.
- **Outlaw enemies** — Enemy outlaws chase the player using directional AI. They have angry faces normally and scared expressions when powered up. Eliminated outlaws respawn after 5 seconds.
- **Sheriff's Badge power-up** — Four badges are hidden in the corners of each maze. Collecting one triggers a 5-second power-up that turns outlaws blue and lets you eliminate them for bonus points.
- **Two levels** — Level 1 features a brown frontier maze with 2 outlaws. Level 2 features a green forest maze with 3 faster outlaws. Lives reset to 3 at the start of each level.
- **Replay system** — After game over or winning, players can press R to replay or Q to quit.
- **Win screen with particles** — Colorful bursting particle effects celebrate beating the game.
- **HUD and screens** — A persistent heads-up display shows score, lives, level, and power-up countdown. Title, level intro, level clear, game over, and win screens are all implemented.

## Design Considerations

The character art is drawn procedurally using Pygame's primitive shape functions (rectangles, circles, polygons, arcs) rather than imported image sprites. This kept the project self-contained and gave full control over the visual style. The cowboy has a brown hat with black outline, a smiling face, and a glowing sheriff badge on his chest when powered up. Outlaws wear black hats and red triangle bandanas, with angry eyebrows that change to wide scared eyes when the power-up is active.

Enemy AI uses a simple heuristic: compare horizontal vs. vertical distance to the player and pick the dominant axis direction. This creates believable chasing behavior without complex pathfinding, and is efficient enough to support multiple enemies without any performance issues.

Each level has a distinct color scheme — brown and tan for Level 1, dark green and light green for Level 2 — to give each stage a different visual feel.

## Challenges

The biggest challenge was getting smooth wall collision to work with pixel-based movement on a tile grid. The solution was checking all four corners of the player's bounding box against wall tiles, with a small inward margin. This prevents clipping while still allowing the player to navigate tight corridors smoothly.

Synthesizing sound effects entirely in code using numpy was a new skill — generating waveforms for different sounds (sine waves for musical tones, noise bursts for gunshots) and shaping them with attack/decay envelopes to make them feel natural.

Managing multiple game states (playing, powered-up, invincible after being caught, between levels, end screen) in a clean and organized way was also a key learning experience.

## Future Improvements

- Animated sprites instead of procedurally drawn shapes
- A high score leaderboard saved to a local file
- More maze levels with increasing complexity
- A main menu with difficulty selection
- Background music
