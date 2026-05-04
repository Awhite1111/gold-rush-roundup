# ============================================================
# GOLD RUSH ROUNDUP - Week 3
# Builds on Week 2. Adds:
#   - Sheriff's Badge power-up (timed invincibility + kill outlaws)
#   - Polished HUD (score, lives, power-up timer)
#   - Proper Game Over screen and Win screen
#   - 2 outlaw enemies
# ============================================================

import pygame
import sys
import random

# --- Constants ---
TILE  = 40
COLS  = 19
ROWS  = 15
WIDTH  = COLS * TILE
HEIGHT = ROWS * TILE
FPS   = 60
POWER_DURATION = 300   # frames (~5 seconds at 60fps)

# Colors
BLACK    = (0,   0,   0)
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

# ── helpers ──────────────────────────────────────────────────

def is_wall_pixel(px, py):
    margin = 4
    for cx, cy in [(px+margin, py+margin),(px+TILE-margin, py+margin),
                   (px+margin, py+TILE-margin),(px+TILE-margin, py+TILE-margin)]:
        col, row = cx // TILE, cy // TILE
        if row < 0 or row >= ROWS or col < 0 or col >= COLS: return True
        if MAZE[row][col] == 1: return True
    return False

# ── drawing ───────────────────────────────────────────────────

def draw_maze(surface):
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col*TILE, row*TILE
            if MAZE[row][col] == 1:
                pygame.draw.rect(surface, BROWN, (x, y, TILE, TILE))
                pygame.draw.rect(surface, BLACK, (x, y, TILE, TILE), 2)
            else:
                pygame.draw.rect(surface, TAN, (x, y, TILE, TILE))


def draw_cowboy(surface, x, y, powered=False):
    cx, cy = x + TILE//2, y + TILE//2
    color = BLUE if powered else BLACK
    pygame.draw.rect(surface, color,          (cx-14, cy-16, 28,  5))
    pygame.draw.rect(surface, color,          (cx- 9, cy-28, 18, 14))
    pygame.draw.circle(surface,(255,220,177), (cx,    cy- 6,  9))
    body_color = BLUE if powered else YELLOW
    pygame.draw.rect(surface, body_color,     (cx- 8, cy+ 3, 16, 14))
    pygame.draw.rect(surface, color,          (cx- 8, cy+17,  7, 10))
    pygame.draw.rect(surface, color,          (cx+ 1, cy+17,  7, 10))
    if powered:
        # glowing star badge
        pygame.draw.circle(surface, YELLOW, (cx+6, cy+6), 5)


def draw_outlaw(surface, x, y, scared=False):
    cx, cy = x + TILE//2, y + TILE//2
    hat_color = BLUE if scared else BLACK
    body_color = BLUE if scared else DARK_RED
    pygame.draw.rect(surface, hat_color, (cx-14, cy-16, 28,  5))
    pygame.draw.rect(surface, hat_color, (cx- 9, cy-28, 18, 14))
    pygame.draw.circle(surface,(200,150,100),(cx, cy-6, 9) if False else (cx,cy-6), 9)
    band_color = BLUE if scared else RED
    pygame.draw.rect(surface, band_color,(cx-9, cy-8, 18, 7))
    pygame.draw.rect(surface, body_color,(cx-8, cy+3, 16, 14))
    pygame.draw.rect(surface, hat_color, (cx-8, cy+17, 7, 10))
    pygame.draw.rect(surface, hat_color, (cx+1, cy+17, 7, 10))


def draw_coin(surface, cx, cy):
    pygame.draw.circle(surface, GOLD,  (cx, cy), 7)
    pygame.draw.circle(surface, YELLOW,(cx, cy), 5)


def draw_badge(surface, cx, cy):
    """Draw a sheriff's badge (star shape)."""
    pygame.draw.circle(surface, SILVER, (cx, cy), 10)
    pygame.draw.circle(surface, GOLD,   (cx, cy),  7)
    pygame.draw.polygon(surface, SILVER, [
        (cx, cy-10),(cx+3,cy-3),(cx+10,cy-3),
        (cx+4,cy+2),(cx+6,cy+9),(cx,cy+5),
        (cx-6,cy+9),(cx-4,cy+2),(cx-10,cy-3),(cx-3,cy-3)
    ])


# ── coin / badge setup ───────────────────────────────────────

def make_coins():
    coins = []
    badge_positions = {(1,4),(17,4),(1,10),(17,10)}   # 4 badge locations
    for row in range(ROWS):
        for col in range(COLS):
            if MAZE[row][col] == 0:
                is_badge = (col, row) in badge_positions
                coins.append({"x": col*TILE+TILE//2, "y": row*TILE+TILE//2,
                               "active": True, "badge": is_badge})
    return coins


# ── outlaw class ─────────────────────────────────────────────

class Outlaw:
    def __init__(self, col, row):
        self.x = float(col * TILE)
        self.y = float(row * TILE)
        self.speed = 1.5
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.move_timer = 0
        self.alive = True

    def update(self, player_x, player_y, scared):
        if not self.alive: return
        self.move_timer += 1
        interval = 60 if scared else 30
        if self.move_timer >= interval:
            self.move_timer = 0
            dx = player_x - self.x
            dy = player_y - self.y
            if scared:   # run away
                dx, dy = -dx, -dy
            if abs(dx) > abs(dy):
                self.dir = (1,0) if dx > 0 else (-1,0)
            else:
                self.dir = (0,1) if dy > 0 else (0,-1)

        nx = self.x + self.dir[0] * self.speed
        ny = self.y + self.dir[1] * self.speed
        if not is_wall_pixel(int(nx), int(self.y)):
            self.x = nx
        else:
            self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        if not is_wall_pixel(int(self.x), int(ny)):
            self.y = ny
        else:
            self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def rect(self):
        return pygame.Rect(int(self.x)+6, int(self.y)+6, TILE-12, TILE-12)

    def respawn(self, col, row):
        self.x = float(col * TILE)
        self.y = float(row * TILE)
        self.alive = True


# ── screens ───────────────────────────────────────────────────

def game_over_screen(screen, font_big, font_sm, score):
    screen.fill((80, 20, 0))
    t1 = font_big.render("GAME OVER", True, RED)
    t2 = font_sm.render(f"Final Score: {score}", True, WHITE)
    t3 = font_sm.render("Press any key to quit", True, TAN)
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2))
    screen.blit(t3, (WIDTH//2 - t3.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()
    wait_key()


def win_screen(screen, font_big, font_sm, score):
    screen.fill((20, 80, 20))
    t1 = font_big.render("YOU WIN, PARTNER!", True, GOLD)
    t2 = font_sm.render(f"Final Score: {score}", True, WHITE)
    t3 = font_sm.render("Press any key to quit", True, TAN)
    screen.blit(t1, (WIDTH//2 - t1.get_width()//2, HEIGHT//2 - 60))
    screen.blit(t2, (WIDTH//2 - t2.get_width()//2, HEIGHT//2))
    screen.blit(t3, (WIDTH//2 - t3.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()
    wait_key()


def wait_key():
    while True:
        for e in pygame.event.get():
            if e.type in (pygame.QUIT, pygame.KEYDOWN):
                return


# ── main ──────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Gold Rush Roundup - Week 3")
    clock = pygame.time.Clock()
    font_big = pygame.font.SysFont("Arial", 36, bold=True)
    font_hud = pygame.font.SysFont("Arial", 18)

    player_x, player_y = 1*TILE, 1*TILE
    speed = 3
    score = 0
    lives = 3
    power_timer = 0
    invincible_timer = 0
    coins = make_coins()
    outlaws = [Outlaw(17, 1), Outlaw(17, 13)]

    running = True
    while running:
        clock.tick(FPS)
        powered = power_timer > 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: running = False

        # --- Movement ---
        keys = pygame.key.get_pressed()
        nx, ny = player_x, player_y
        if keys[pygame.K_LEFT]:  nx -= speed
        if keys[pygame.K_RIGHT]: nx += speed
        if keys[pygame.K_UP]:    ny -= speed
        if keys[pygame.K_DOWN]:  ny += speed
        if not is_wall_pixel(nx, player_y): player_x = nx
        if not is_wall_pixel(player_x, ny): player_y = ny

        # --- Power-up timer ---
        if power_timer > 0:
            power_timer -= 1

        # --- Coin / badge collection ---
        p_cx = player_x + TILE//2
        p_cy = player_y + TILE//2
        for coin in coins:
            if coin["active"] and abs(p_cx-coin["x"]) < 14 and abs(p_cy-coin["y"]) < 14:
                coin["active"] = False
                if coin["badge"]:
                    power_timer = POWER_DURATION
                    score += 50
                else:
                    score += 10

        # --- Outlaw update & collision ---
        p_rect = pygame.Rect(player_x+4, player_y+4, TILE-8, TILE-8)
        for outlaw in outlaws:
            outlaw.update(player_x, player_y, powered)
            if not outlaw.alive: continue
            if p_rect.colliderect(outlaw.rect()):
                if powered:
                    outlaw.alive = False
                    score += 200
                elif invincible_timer == 0:
                    lives -= 1
                    invincible_timer = 90
                    player_x, player_y = 1*TILE, 1*TILE
                    if lives <= 0:
                        game_over_screen(screen, font_big, font_hud, score)
                        running = False

        if invincible_timer > 0:
            invincible_timer -= 1

        # --- Win check ---
        if all(not c["active"] for c in coins):
            win_screen(screen, font_big, font_hud, score)
            running = False

        # --- Draw ---
        screen.fill(SKY_BLUE)
        draw_maze(screen)

        for coin in coins:
            if coin["active"]:
                if coin["badge"]:
                    draw_badge(screen, coin["x"], coin["y"])
                else:
                    draw_coin(screen, coin["x"], coin["y"])

        for outlaw in outlaws:
            if outlaw.alive:
                draw_outlaw(screen, int(outlaw.x), int(outlaw.y), scared=powered)

        if invincible_timer == 0 or (invincible_timer//6) % 2 == 0:
            draw_cowboy(screen, player_x, player_y, powered=powered)

        # HUD bar background
        pygame.draw.rect(screen, (50,30,10), (0, 0, WIDTH, 28))
        coins_left = sum(1 for c in coins if c["active"] and not c["badge"])
        hud = font_hud.render(
            f"Score: {score}   Lives: {'★'*lives}   Coins: {coins_left}"
            + (f"   ⚡ BADGE: {power_timer//60+1}s" if powered else ""),
            True, GOLD)
        screen.blit(hud, (8, 5))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
