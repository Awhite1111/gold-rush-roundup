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

# ============================================================
# GOLD RUSH ROUNDUP - Week 1
# Goal: Set up Pygame window, draw tile-based maze,
#       implement cowboy player with arrow key movement
#       and wall collision.
# ============================================================

import pygame
import sys

# --- Constants ---
TILE = 40           # size of each maze tile in pixels
COLS = 19           # number of columns
ROWS = 15           # number of rows
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE
FPS = 60

# Colors
BLACK       = (0,   0,   0)
WHITE       = (255, 255, 255)
BROWN       = (139, 90,  43)
TAN         = (210, 180, 140)
YELLOW      = (255, 215,  0)
SKY_BLUE    = (135, 206, 235)

# Maze layout  (1 = wall, 0 = open path)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,0,0,1,1,1,0,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

def draw_maze(surface):
    """Draw the tile-based maze grid."""
    for row in range(ROWS):
        for col in range(COLS):
            x = col * TILE
            y = row * TILE
            if MAZE[row][col] == 1:
                # Draw a wooden wall block
                pygame.draw.rect(surface, BROWN, (x, y, TILE, TILE))
                pygame.draw.rect(surface, BLACK, (x, y, TILE, TILE), 2)
            else:
                # Draw dusty ground
                pygame.draw.rect(surface, TAN, (x, y, TILE, TILE))


def draw_cowboy(surface, x, y):
    """Draw a simple cowboy shape at pixel position (x, y)."""
    cx = x + TILE // 2
    cy = y + TILE // 2

    # Hat brim
    pygame.draw.rect(surface, BLACK, (cx - 14, cy - 16, 28, 5))
    # Hat top
    pygame.draw.rect(surface, BLACK, (cx - 9, cy - 28, 18, 14))
    # Head
    pygame.draw.circle(surface, (255, 220, 177), (cx, cy - 6), 9)
    # Body
    pygame.draw.rect(surface, YELLOW, (cx - 8, cy + 3, 16, 14))
    # Legs
    pygame.draw.rect(surface, BLACK, (cx - 8, cy + 17, 7, 10))
    pygame.draw.rect(surface, BLACK, (cx + 1, cy + 17, 7, 10))

def get_tile(pixel_x, pixel_y):
    """Convert pixel coordinates to tile (col, row)."""
    return pixel_x // TILE, pixel_y // TILE

def is_wall(pixel_x, pixel_y):
    """Check if the four corners of a tile-sized box hit a wall."""
    margin = 4  # how close to walls we allow
    corners = [
        (pixel_x + margin,        pixel_y + margin),
        (pixel_x + TILE - margin, pixel_y + margin),
        (pixel_x + margin,        pixel_y + TILE - margin),
        (pixel_x + TILE - margin, pixel_y + TILE - margin),
    ]
    for (cx, cy) in corners:
        col, row = cx // TILE, cy // TILE
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return True
        if MAZE[row][col] == 1:
            return True
    return False

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gold Rush Roundup - Week 1")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    # Start cowboy at tile (1,1)
    player_x = 1 * TILE
    player_y = 1 * TILE
    speed = 3

    running = True
    while running:
        clock.tick(FPS)

        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- Movement ---
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y

        if keys[pygame.K_LEFT]:
            new_x -= speed
        if keys[pygame.K_RIGHT]:
            new_x += speed
        if keys[pygame.K_UP]:
            new_y -= speed
        if keys[pygame.K_DOWN]:
            new_y += speed

        # Only move if new position isn't a wall
        if not is_wall(new_x, player_y):
            player_x = new_x
        if not is_wall(player_x, new_y):
            player_y = new_y

        # --- Draw ---
        screen.fill(SKY_BLUE)
        draw_maze(screen)
        draw_cowboy(screen, player_x, player_y)

        # HUD
        label = font.render("Week 1 - Move with Arrow Keys | ESC to quit", True, BLACK)
        screen.blit(label, (8, 4))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
