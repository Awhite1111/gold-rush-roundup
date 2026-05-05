# ============================================================
# GOLD RUSH ROUNDUP - Final Project (Week 4)
# src/project.py
#
# A Wild West Pac-Man style maze game built with Pygame.
# Collect all gold coins, grab Sheriff Badges for power-ups,
# and avoid (or eliminate!) outlaw enemies across 2 levels.
#
# Controls: Arrow Keys to move | ESC to quit
# ============================================================

import pygame
import sys
import random
import numpy as np

# ── Constants ────────────────────────────────────────────────
TILE   = 40
COLS   = 19
ROWS   = 15
WIDTH  = COLS * TILE
HEIGHT = ROWS * TILE + 30   # extra 30px for HUD
FPS    = 60
POWER_DURATION = 300        # frames (~5 sec)

# Colors
BLACK    = (  0,   0,   0)
WHITE    = (255, 255, 255)
BROWN    = (139,  90,  43)
TAN      = (210, 180, 140)
YELLOW   = (255, 215,   0)
GOLD     = (255, 185,   0)
RED      = (200,  30,  30)
DARK_RED = (139,   0,   0)
SKY_BLUE = (135, 206, 235)
SILVER   = (192, 192, 192)
BLUE     = ( 30,  30, 200)
ORANGE   = (255, 140,   0)
DARK_BG  = ( 50,  30,  10)
GREEN    = ( 20, 140,  20)

# ── Maze layouts (1=wall, 0=path) ────────────────────────────
LEVEL_1 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [0,0,1,1,0,1,1,1,0,0,0,1,1,1,0,1,1,0,0],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

LEVEL_2 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,1,1,0,1,0,1,0,1,0,1],
    [1,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

LEVELS       = [LEVEL_1, LEVEL_2]
ENEMY_COUNTS = [2, 3]
ENEMY_SPEEDS = [1.5, 2.0]
BADGE_SPOTS  = [{(1,4),(17,4),(1,10),(17,10)},
                {(1,1),(17,1),(1,13),(17,13)}]


# ── Sound generation ─────────────────────────────────────────

def make_sound(frequency, duration_ms, volume=0.4, wave="sine", fade_ms=10):
    """Generate a simple synthesized sound using numpy and pygame."""
    sample_rate = 44100
    n_samples   = int(sample_rate * duration_ms / 1000)
    t = np.linspace(0, duration_ms / 1000, n_samples, endpoint=False)

    if wave == "sine":
        samples = np.sin(2 * np.pi * frequency * t)
    elif wave == "square":
        samples = np.sign(np.sin(2 * np.pi * frequency * t))
    elif wave == "sawtooth":
        samples = 2 * (t * frequency - np.floor(t * frequency + 0.5))
    else:
        samples = np.sin(2 * np.pi * frequency * t)

    # Simple fade-out to avoid clicks
    fade_samples = int(sample_rate * fade_ms / 1000)
    if fade_samples < n_samples:
        fade = np.ones(n_samples)
        fade[-fade_samples:] = np.linspace(1, 0, fade_samples)
        samples *= fade

    samples = (samples * volume * 32767).astype(np.int16)
    stereo  = np.column_stack([samples, samples])
    return pygame.sndarray.make_sound(stereo)


def make_coin_sound():
    """Short high-pitched 'ding' for collecting a coin."""
    sample_rate = 44100
    dur = 0.12
    n   = int(sample_rate * dur)
    t   = np.linspace(0, dur, n, endpoint=False)
    # Two-tone chord: 880 Hz + 1320 Hz
    s   = 0.5 * np.sin(2 * np.pi * 880  * t) \
        + 0.5 * np.sin(2 * np.pi * 1320 * t)
    fade = np.linspace(1, 0, n)
    s   = (s * fade * 0.4 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([s, s]))


def make_badge_sound():
    """Rising arpeggio for grabbing the Sheriff's Badge."""
    sample_rate = 44100
    freqs = [523, 659, 784, 1047]   # C5 E5 G5 C6
    parts = []
    for f in freqs:
        dur = 0.09
        n   = int(sample_rate * dur)
        t   = np.linspace(0, dur, n, endpoint=False)
        s   = np.sin(2 * np.pi * f * t)
        fade = np.linspace(1, 0, n)
        parts.append(s * fade)
    full = np.concatenate(parts)
    full = (full * 0.45 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([full, full]))


def make_hit_sound():
    """Low thud / buzz when caught by an outlaw."""
    sample_rate = 44100
    dur = 0.35
    n   = int(sample_rate * dur)
    t   = np.linspace(0, dur, n, endpoint=False)
    # Descending pitch sweep
    freq = np.linspace(300, 80, n)
    s    = np.sign(np.sin(2 * np.pi * np.cumsum(freq) / sample_rate))
    fade = np.linspace(1, 0, n)
    s    = (s * fade * 0.45 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([s, s]))


def make_zap_sound():
    """Western gunshot sound when eliminating a scared outlaw."""
    sample_rate = 44100
    dur = 0.3
    n   = int(sample_rate * dur)
    t   = np.linspace(0, dur, n, endpoint=False)
    # Sharp noise burst for the crack
    noise = np.random.uniform(-1, 1, n)
    # Fast attack, slow decay envelope
    env = np.exp(-t * 18)
    # Low frequency rumble underneath
    rumble = np.sin(2 * np.pi * 80 * t) * np.exp(-t * 12)
    s = (noise * env * 0.7) + (rumble * 0.3)
    s = (s * 0.6 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([s, s]))


def make_level_clear_sound():
    """Cheerful ascending fanfare for clearing a level."""
    sample_rate = 44100
    # C4 E4 G4 C5 — each note a bit longer
    notes = [(262, 0.12), (330, 0.12), (392, 0.12), (523, 0.28)]
    parts = []
    for f, dur in notes:
        n  = int(sample_rate * dur)
        t  = np.linspace(0, dur, n, endpoint=False)
        s  = np.sin(2 * np.pi * f * t)
        fade = np.linspace(1, 0, n)
        parts.append(s * fade)
    full = np.concatenate(parts)
    full = (full * 0.5 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([full, full]))


def make_game_over_sound():
    """Sad descending wah-wah for game over."""
    sample_rate = 44100
    notes = [(392, 0.18), (330, 0.18), (262, 0.18), (196, 0.40)]
    parts = []
    for f, dur in notes:
        n  = int(sample_rate * dur)
        t  = np.linspace(0, dur, n, endpoint=False)
        s  = np.sin(2 * np.pi * f * t)
        fade = np.linspace(1, 0, n)
        parts.append(s * fade)
    full = np.concatenate(parts)
    full = (full * 0.5 * 32767).astype(np.int16)
    return pygame.sndarray.make_sound(np.column_stack([full, full]))


def init_sounds():
    """Initialise pygame mixer and build all sound effects. Returns a dict."""
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    return {
        "coin":        make_coin_sound(),
        "badge":       make_badge_sound(),
        "hit":         make_hit_sound(),
        "zap":         make_zap_sound(),
        "level_clear": make_level_clear_sound(),
        "game_over":   make_game_over_sound(),
    }


# ── Utility ──────────────────────────────────────────────────

def is_wall_pixel(px, py, maze):
    margin = 4
    for cx, cy in [(px+margin, py+margin),(px+TILE-margin, py+margin),
                   (px+margin, py+TILE-margin),(px+TILE-margin, py+TILE-margin)]:
        col, row = cx // TILE, cy // TILE
        if row < 0 or row >= ROWS or col < 0 or col >= COLS:
            return True
        if maze[row][col] == 1:
            return True
    return False


# ── Drawing helpers ───────────────────────────────────────────

DARK_GREEN  = ( 34,  85,  34)
LIGHT_GREEN = (144, 188, 144)

def draw_maze(surface, maze, level_index=0):
    wall_color  = DARK_GREEN  if level_index == 1 else BROWN
    floor_color = LIGHT_GREEN if level_index == 1 else TAN
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col*TILE, row*TILE + 30
            if maze[row][col] == 1:
                pygame.draw.rect(surface, wall_color,  (x, y, TILE, TILE))
                pygame.draw.rect(surface, BLACK,       (x, y, TILE, TILE), 2)
            else:
                pygame.draw.rect(surface, floor_color, (x, y, TILE, TILE))


def draw_cowboy(surface, x, y, powered=False):
    """Draw the player cowboy character."""
    cx, cy = x + TILE//2, y + TILE//2 + 30
    # Hat brim
    pygame.draw.rect(surface,   BROWN,        (cx-14, cy-16, 28,  5))
    pygame.draw.rect(surface,   BLACK,        (cx-14, cy-16, 28,  5), 1)
    # Hat top
    pygame.draw.rect(surface,   BROWN,        (cx- 9, cy-28, 18, 14))
    pygame.draw.rect(surface,   BLACK,        (cx- 9, cy-28, 18, 14), 1)
    pygame.draw.circle(surface, (255,220,177),(cx,    cy- 6),  9)
    # Eyes
    pygame.draw.circle(surface, BLACK, (cx - 3, cy - 8), 2)
    pygame.draw.circle(surface, BLACK, (cx + 3, cy - 8), 2)
    # Smile
    pygame.draw.arc(surface, BLACK, pygame.Rect(cx - 4, cy - 5, 8, 5), 3.14, 0, 2)
    pygame.draw.rect(surface,   YELLOW,       (cx- 8, cy+ 3, 16, 14))
    # Left boot
    pygame.draw.rect(surface,   BROWN,        (cx- 8, cy+17,  7, 10))
    pygame.draw.rect(surface,   BLACK,        (cx- 8, cy+17,  7, 10), 1)
    # Right boot
    pygame.draw.rect(surface,   BROWN,        (cx+ 1, cy+17,  7, 10))
    pygame.draw.rect(surface,   BLACK,        (cx+ 1, cy+17,  7, 10), 1)
    if powered:
        # Glowing sheriff badge on chest
        pygame.draw.circle(surface, ORANGE, (cx+6, cy+6), 6)
        pygame.draw.circle(surface, YELLOW, (cx+6, cy+6), 4)
        # Black star on badge
        bx, by2 = cx+6, cy+6
        pts = [(bx,by2-4),(bx+1,by2-1),(bx+4,by2-1),(bx+2,by2+1),
               (bx+3,by2+4),(bx,by2+2),(bx-3,by2+4),(bx-2,by2+1),
               (bx-4,by2-1),(bx-1,by2-1)]
        pygame.draw.polygon(surface, BLACK, pts)


def draw_outlaw(surface, x, y, scared=False):
    """Draw an outlaw enemy character."""
    cx, cy = x + TILE//2, y + TILE//2 + 30
    hat  = BLUE    if scared else BLACK
    body = BLUE    if scared else DARK_RED
    band = BLUE    if scared else RED
    pygame.draw.rect(surface,   hat,          (cx-14, cy-16, 28,  5))
    pygame.draw.rect(surface,   hat,          (cx- 9, cy-28, 18, 14))
    pygame.draw.circle(surface, (200,150,100),(cx,    cy- 6),  9)
    pygame.draw.rect(surface,   body,         (cx- 8, cy+ 3, 16, 14))
    pygame.draw.rect(surface,   hat,          (cx- 8, cy+17,  7, 10))
    pygame.draw.rect(surface,   hat,          (cx+ 1, cy+17,  7, 10))
    # Bandana as triangle
    if not scared:
        pygame.draw.polygon(surface, RED, [(cx-9, cy-8), (cx+9, cy-8), (cx, cy+1)])
    else:
        pygame.draw.polygon(surface, BLUE, [(cx-9, cy-8), (cx+9, cy-8), (cx, cy+1)])
    if scared:
        # Scared face - wide eyes and worried mouth
        pygame.draw.circle(surface, WHITE, (cx - 3, cy - 8), 3)
        pygame.draw.circle(surface, WHITE, (cx + 3, cy - 8), 3)
        pygame.draw.circle(surface, BLACK, (cx - 3, cy - 8), 1)
        pygame.draw.circle(surface, BLACK, (cx + 3, cy - 8), 1)
        pygame.draw.arc(surface, BLACK, pygame.Rect(cx - 4, cy - 4, 8, 5), 0, 3.14, 2)
    else:
        # Angry face - mean eyes and scowl
        pygame.draw.circle(surface, BLACK, (cx - 3, cy - 8), 2)
        pygame.draw.circle(surface, BLACK, (cx + 3, cy - 8), 2)
        pygame.draw.line(surface, BLACK, (cx - 5, cy - 11), (cx - 1, cy - 9), 2)
        pygame.draw.line(surface, BLACK, (cx + 5, cy - 11), (cx + 1, cy - 9), 2)
        pygame.draw.arc(surface, BLACK, pygame.Rect(cx - 4, cy - 3, 8, 5), 0, 3.14, 2)


def draw_coin(surface, cx, cy):
    pygame.draw.circle(surface, GOLD,  (cx, cy+30), 7)
    pygame.draw.circle(surface, YELLOW,(cx, cy+30), 5)


def draw_badge(surface, cx, cy):
    """Draw a collectible sheriff's badge."""
    by = cy + 30
    pygame.draw.circle(surface, ORANGE, (cx, by), 10)
    pygame.draw.circle(surface, YELLOW, (cx, by),  7)
    pts = [(cx,by-10),(cx+3,by-3),(cx+10,by-3),(cx+4,by+2),
           (cx+6,by+9),(cx,by+5),(cx-6,by+9),(cx-4,by+2),
           (cx-10,by-3),(cx-3,by-3)]
    pygame.draw.polygon(surface, BLACK, pts)


def draw_hud(surface, font, score, lives, level, power_timer, coins_left):
    """Draw the top HUD bar."""
    pygame.draw.rect(surface, DARK_BG, (0, 0, WIDTH, 30))
    powered = power_timer > 0
    badge_text = f"  ⚡{power_timer//60+1}s" if powered else ""
    text = (f"Level {level+1}   Score: {score}   "
            f"Lives: {lives}   "
            f"Coins: {coins_left}{badge_text}")
    hud = font.render(text, True, GOLD)
    surface.blit(hud, (8, 6))


# ── Collectibles ─────────────────────────────────────────────

def make_coins(maze, badge_spots):
    """Build the list of coins and badges for a level."""
    items = []
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 0:
                is_badge = (col, row) in badge_spots
                items.append({
                    "x": col*TILE + TILE//2,
                    "y": row*TILE + TILE//2,
                    "active": True,
                    "badge": is_badge
                })
    return items


# ── Outlaw enemy ─────────────────────────────────────────────

class Outlaw:
    def __init__(self, col, row, speed):
        self.x          = float(col * TILE)
        self.y          = float(row * TILE)
        self.start_col  = col
        self.start_row  = row
        self.speed      = speed
        self.dir        = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.timer      = 0
        self.alive      = True
        self.respawn_timer = 0

    def update(self, px, py, scared, maze):
        """Move the outlaw; chase player normally, flee when scared."""
        if not self.alive:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.x = float(self.start_col * TILE)
                self.y = float(self.start_row * TILE)
                self.alive = True
            return
        self.timer += 1
        interval = 60 if scared else 25
        if self.timer >= interval:
            self.timer = 0
            dx = px - self.x
            dy = py - self.y
            if scared:
                dx, dy = -dx, -dy
            if abs(dx) > abs(dy):
                self.dir = (1,0) if dx > 0 else (-1,0)
            else:
                self.dir = (0,1) if dy > 0 else (0,-1)

        nx = self.x + self.dir[0] * self.speed
        ny = self.y + self.dir[1] * self.speed
        if not is_wall_pixel(int(nx), int(self.y), maze):
            self.x = nx
        else:
            self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        if not is_wall_pixel(int(self.x), int(ny), maze):
            self.y = ny
        else:
            self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def get_rect(self):
        return pygame.Rect(int(self.x)+6, int(self.y)+6+30, TILE-12, TILE-12)


def make_outlaws(level_index):
    """Create outlaws for a given level."""
    starts = [(17,1),(17,13),(1,13),(9,7),(1,7)]
    count  = ENEMY_COUNTS[level_index]
    speed  = ENEMY_SPEEDS[level_index]
    return [Outlaw(starts[i][0], starts[i][1], speed) for i in range(count)]


# ── Screen helpers ───────────────────────────────────────────

def fade_message(screen, font_big, font_sm, line1, line2, color1=GOLD, bg=(50,30,10)):
    """Show a full-screen message and wait for keypress."""
    screen.fill(bg)
    t1 = font_big.render(line1, True, color1)
    t2 = font_sm.render(line2,  True, WHITE)
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 50))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 + 20))
    pygame.display.flip()
    _wait_key()


def end_screen(screen, font_big, font_sm, title, score, color, bg):
    """Show game over or win screen with particles on win. Returns True to replay, False to quit."""
    is_win = color == GOLD
    particles = []
    if is_win:
        for _ in range(80):
            particles.append({
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "vx": random.uniform(-3, 3),
                "vy": random.uniform(-5, -1),
                "color": random.choice([GOLD, YELLOW, ORANGE, WHITE, RED]),
                "size": random.randint(3, 8),
                "life": random.randint(40, 120)
            })

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill(bg)

        if is_win:
            for p in particles:
                pygame.draw.circle(screen, p["color"], (int(p["x"]), int(p["y"])), p["size"])
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["vy"] += 0.1  # gravity
                p["life"] -= 1
                if p["life"] <= 0:
                    p["x"] = random.randint(0, WIDTH)
                    p["y"] = HEIGHT + 10
                    p["vx"] = random.uniform(-3, 3)
                    p["vy"] = random.uniform(-8, -3)
                    p["color"] = random.choice([GOLD, YELLOW, ORANGE, WHITE, RED])
                    p["size"] = random.randint(3, 8)
                    p["life"] = random.randint(40, 120)

        t1 = font_big.render(title, True, color)
        t2 = font_sm.render(f"Final Score: {score}", True, WHITE)
        t3 = font_sm.render("Press R to Replay   |   Press Q to Quit", True, TAN)
        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 80))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2 - 10))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, HEIGHT//2 + 50))
        pygame.display.flip()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_q:
                    return False


def _wait_key():
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN):
                return


def title_screen(screen, font_big, font_sm):
    """Show a simple title / start screen."""
    screen.fill((80, 50, 10))
    title  = font_big.render("GOLD RUSH ROUNDUP", True, GOLD)
    sub    = font_sm.render("Collect all gold coins — avoid the outlaws!", True, TAN)
    start  = font_sm.render("Press any key to begin...", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 80))
    screen.blit(sub,   (WIDTH//2 - sub.get_width()//2,   HEIGHT//2 - 20))
    screen.blit(start, (WIDTH//2 - start.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()
    _wait_key()


# ── Level loop ───────────────────────────────────────────────

def run_level(screen, clock, fonts, sounds, level_index, score, lives):
    """
    Run a single level. Returns (score, lives, completed).
    completed=True means all coins collected; False means game over.
    """
    font_big, font_hud = fonts
    maze        = LEVELS[level_index]
    coins       = make_coins(maze, BADGE_SPOTS[level_index])
    outlaws     = make_outlaws(level_index)
    player_x    = 1 * TILE
    player_y    = 1 * TILE
    speed       = 3
    power_timer = 0
    inv_timer   = 0   # brief invincibility after being caught
    lives       = 3   # reset lives each level

    fade_message(screen, font_big, font_hud,
                 f"LEVEL {level_index + 1}",
                 "Collect all gold coins!  Press any key...",
                 GOLD, (30, 20, 5))

    running = True
    while running:
        clock.tick(FPS)
        powered = power_timer > 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()

        # --- Player movement ---
        keys = pygame.key.get_pressed()
        nx, ny = player_x, player_y
        if keys[pygame.K_LEFT]:  nx -= speed
        if keys[pygame.K_RIGHT]: nx += speed
        if keys[pygame.K_UP]:    ny -= speed
        if keys[pygame.K_DOWN]:  ny += speed

        # --- Screen wrapping left/right (before wall check) ---
        if nx < 0:
            player_x = WIDTH - TILE
            nx = player_x
        elif nx >= WIDTH - TILE:
            player_x = 0
            nx = player_x

        if not is_wall_pixel(nx, player_y, maze): player_x = nx
        if not is_wall_pixel(player_x, ny, maze): player_y = ny

        # --- Power-up countdown ---
        if power_timer > 0:
            power_timer -= 1

        # --- Collect coins / badges ---
        pcx = player_x + TILE//2
        pcy = player_y + TILE//2
        for item in coins:
            if item["active"] and abs(pcx-item["x"]) < 14 and abs(pcy-item["y"]) < 14:
                item["active"] = False
                if item["badge"]:
                    power_timer = POWER_DURATION
                    score += 50
                    sounds["badge"].play()
                else:
                    score += 10
                    sounds["coin"].play()

        # --- Update outlaws & collisions ---
        p_rect = pygame.Rect(player_x+4, player_y+4+30, TILE-8, TILE-8)
        if inv_timer > 0:
            inv_timer -= 1

        for outlaw in outlaws:
            outlaw.update(player_x, player_y, powered, maze)
            if not outlaw.alive:
                continue
            if p_rect.colliderect(outlaw.get_rect()):
                if powered:
                    outlaw.alive = False
                    outlaw.respawn_timer = 300  # respawn after ~5 seconds
                    score += 200
                    sounds["zap"].play()
                elif inv_timer == 0:
                    lives -= 1
                    inv_timer = 90
                    player_x, player_y = 9*TILE, 7*TILE
                    sounds["hit"].play()
                    if lives <= 0:
                        sounds["game_over"].play()
                        pygame.time.wait(500)
                        return score, 0, False

        # --- Win check ---
        coins_left = sum(1 for c in coins if c["active"] and not c["badge"])
        if coins_left == 0:
            sounds["level_clear"].play()
            pygame.time.wait(800)
            return score, lives, True

        # --- Draw ---
        screen.fill(SKY_BLUE)
        draw_hud(screen, font_hud, score, lives, level_index,
                 power_timer, coins_left)
        draw_maze(screen, maze, level_index)

        for item in coins:
            if item["active"]:
                if item["badge"]:
                    draw_badge(screen, item["x"], item["y"])
                else:
                    draw_coin(screen,  item["x"], item["y"])

        for outlaw in outlaws:
            if outlaw.alive:
                draw_outlaw(screen, int(outlaw.x), int(outlaw.y), scared=powered)

        if inv_timer == 0 or (inv_timer//6) % 2 == 0:
            draw_cowboy(screen, player_x, player_y, powered=powered)

        pygame.display.flip()

    return score, lives, False


# ── Main entry point ─────────────────────────────────────────

def main():
    """Main function — initialises Pygame, runs title + levels."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED | pygame.FULLSCREEN)
    pygame.display.set_caption("Gold Rush Roundup")
    clock    = pygame.time.Clock()
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font_hud = pygame.font.SysFont("Arial", 16)
    fonts    = (font_big, font_hud)
    sounds   = init_sounds()

    while True:
        title_screen(screen, font_big, font_hud)
        score = 0
        lives = 3
        game_over = False

        for level_index in range(len(LEVELS)):
            score, lives, completed = run_level(
                screen, clock, fonts, sounds, level_index, score, lives)

            if not completed:
                game_over = True
                break

            if level_index < len(LEVELS) - 1:
                fade_message(screen, font_big, font_hud,
                             f"LEVEL {level_index+1} CLEARED!",
                             f"Score: {score}   Get ready for Level {level_index+2}...",
                             GOLD, (20, 50, 20))

        if game_over:
            replay = end_screen(screen, font_big, font_hud,
                                "GAME OVER, PARTNER!",
                                score, RED, (60, 10, 10))
        else:
            replay = end_screen(screen, font_big, font_hud,
                                "YOU WIN, PARTNER!",
                                score, GOLD, (20, 60, 20))

        if not replay:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    main()
