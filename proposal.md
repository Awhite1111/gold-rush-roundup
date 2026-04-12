# Gold Rush Roundup

## Repository
<https://github.com/Awhite1111/gold-rush-roundup>

## Description
Gold Rush Roundup is a Pac-Man inspired 2D maze game built in Python where you play as a cowboy navigating a frontier town, collecting gold coins while evading outlaw enemies. It is relevant to digital arts & media as it combines interactive game design, pixel-style visual art, and real-time player mechanics into an original arcade experience.

## Features
- **Cowboy Player Character** - A cowboy sprite controlled by arrow keys that moves through a grid-based maze representing a western frontier town, executed using Pygame's sprite and event systems.
- **Gold Coin Collectibles** - Gold coins scattered throughout the maze that the cowboy collects for points, implemented as a sprite group that checks for collision with the player each frame.
- **Outlaw Enemies** - Enemy outlaw sprites that patrol the maze and chase the player, implemented using simple pathfinding logic (e.g. always move toward the player's grid position).
- **Sheriff's Badge Power-Up** - A collectible badge that temporarily makes the cowboy invincible and able to eliminate outlaws on contact, toggled via a timed game state flag.
- **Score & Lives System** - A HUD displaying the player's current score, remaining lives, and current level, drawn each frame using Pygame's font rendering.
- **Level Progression** - Each level increases enemy speed and maze complexity, implemented by loading new maze layouts from a list of predefined grid arrays.

## Challenges
- Learning how to design and render a tile-based maze grid using Pygame's drawing tools.
- Researching basic enemy AI / pathfinding to make outlaws chase the player in a believable way.
- Understanding sprite collision detection in Pygame for both coin collection and enemy contact.
- Learning how to manage multiple game states (playing, power-up active, game over, level complete).

## Outcomes

**Ideal Outcome:**
- A fully playable multi-level Wild West maze game with a cowboy player, animated outlaw enemies, coin collection, a working power-up system, sound effects, and a score/lives HUD that feels polished and fun to play.

**Minimal Viable Outcome:**
- A single-level playable maze where the cowboy can move through the frontier town, collect all gold coins to win, and must avoid at least one outlaw enemy — with a visible score counter and a game over screen when caught.

## Milestones

- **Week 1**
  1. Set up the Pygame project, create the game window, and render a basic tile-based maze grid.
  2. Implement the cowboy player sprite with arrow key movement and wall collision.

- **Week 2**
  1. Add gold coins to the maze and implement collection logic with a score counter.
  2. Create at least one outlaw enemy sprite with basic movement and player collision (lose a life).

- **Week 3**
  1. Implement the Sheriff's Badge power-up with a timed invincibility state.
  2. Add a HUD (score, lives) and build game over / win screens.

- **Week 4 (Final)**
  1. Add level progression with at least 2 unique maze layouts and increasing difficulty.
  2. Polish sprites, add sound effects, test for bugs, and finalize submission.
