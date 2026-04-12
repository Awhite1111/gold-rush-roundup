# Gold Rush Roundup

**Demo Video:** [YouTube Link — add yours here]
**Repository:** https://github.com/Awhite1111/gold-rush-roundup

## Description

Gold Rush Roundup is a Wild West themed maze game inspired by Pac-Man, built entirely in Python using the Pygame library. You play as a cowboy navigating a frontier town maze, collecting gold coins while avoiding outlaw enemies. Grab a Sheriff's Badge to turn the tables and hunt down the outlaws yourself! The game features two progressively harder levels and a full HUD with score and lives tracking.

This project is relevant to digital arts and media because it combines interactive game design, real-time sprite-based animation, procedural level layout, and player-driven visual storytelling — all core elements of game art and interactive media.

## Files

- `src/project.py` — The main game source file. Contains all game logic, drawing functions, the Outlaw class, level loop, and the main entry point.
- `requirements.txt` — Lists the one third-party library needed to run the game: `pygame`.
- `README.md` — This file. Explains the project, design decisions, and future improvements.

## How to Run

1. Install the requirement:
   ```
   pip install pygame
   ```
2. From the root of the repository, run:
   ```
   python src/project.py
   ```
3. Use **Arrow Keys** to move the cowboy. Press **ESC** to quit at any time.

## Features

- - **Procedurally generated sound effects** — All audio is synthesized at runtime using numpy waveforms (no external audio files). Includes distinct sounds for coin collection, badge pickup, outlaw elimination, taking a hit, level clear, and game over.
- **Tile-based maze** — A grid-based frontier town layout rendered with Pygame's drawing tools, with wall collision detection using corner-based pixel checking.
- **Gold coin collection** — Coins fill every open tile. Collecting all coins on a level advances you to the next.
- **Outlaw enemies** — Enemy outlaws chase the player using directional AI that targets the player's position every few frames. Level 2 adds a third outlaw and increases their speed.
- **Sheriff's Badge power-up** — Four badges are hidden in the corners of each maze. Collecting one triggers a 5-second power-up that turns outlaws blue and lets you eliminate them for bonus points.
- **Two levels** — Level 1 features a classic symmetrical maze with 2 outlaws. Level 2 features a denser maze layout with 3 faster outlaws.
- **HUD and screens** — A persistent heads-up display shows score, lives, level, and power-up countdown. Title, level intro, level clear, game over, and win screens are all implemented.

## Design Considerations

The character art is drawn procedurally using Pygame's primitive shape functions (rectangles, circles, polygons) rather than imported image sprites. This kept the project self-contained and gave me full control over the visual style. The cowboy turns blue when powered up, and outlaws flash blue when scared — giving the player immediate visual feedback.

Enemy AI uses a simple heuristic: compare horizontal vs. vertical distance to the player and pick the dominant axis direction. This creates believable chasing behavior without complex pathfinding, and is efficient enough to support multiple enemies without any performance issues.

## Challenges

The biggest challenge was getting smooth wall collision to work with pixel-based movement on a tile grid. The solution was checking all four corners of the player's bounding box against wall tiles, with a small inward margin. This prevents clipping while still allowing the player to navigate tight corridors smoothly.

Learning to manage multiple game states (playing, powered-up, invincible after being caught, between levels) in a clean way was also a key challenge and learning experience.

## Future Improvements

- Animated sprites instead of procedurally drawn shapes
- A high score leaderboard saved to a local file
- More maze levels with increasing complexity
- A main menu with difficulty selection
