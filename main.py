import pygame
import sys
import random
import math
from entities import Player, Asteroid, Bullet

# --- Constants ---
SCREEN_W, SCREEN_H = 800, 600
FPS = 60
VICTORY_SCORE = 500

# States
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
VICTORY = "victory"

# Colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
YELLOW = (255, 220, 0)
CYAN   = (0, 200, 255)
RED    = (220, 60, 60)
GREEN  = (60, 220, 100)
GRAY   = (180, 180, 180)
DARK   = (15, 15, 30)


# --- Stars (two-layer parallax) ---

def make_stars():
    stars = []
    for _ in range(80):   # far layer: slow, dim
        stars.append({
            'x': random.uniform(0, SCREEN_W),
            'y': random.uniform(0, SCREEN_H),
            'speed': random.uniform(0.2, 0.6),
            'brightness': random.randint(70, 140),
            'size': 1,
        })
    for _ in range(35):   # near layer: faster, brighter
        stars.append({
            'x': random.uniform(0, SCREEN_W),
            'y': random.uniform(0, SCREEN_H),
            'speed': random.uniform(0.9, 2.0),
            'brightness': random.randint(160, 255),
            'size': random.choice([1, 1, 2]),
        })
    return stars


def update_stars(stars, dt):
    for s in stars:
        s['y'] += s['speed']
        if s['y'] > SCREEN_H + 2:
            s['y'] = -2.0
            s['x'] = random.uniform(0, SCREEN_W)


def draw_stars(surface, stars):
    for s in stars:
        b = s['brightness']
        pygame.draw.circle(surface, (b, b, b), (int(s['x']), int(s['y'])), s['size'])


# --- Explosion particles ---

def spawn_explosion(particles, x, y, color):
    for _ in range(14):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(40, 160)
        max_lt = random.uniform(0.28, 0.55)
        particles.append({
            'x': float(x), 'y': float(y),
            'vx': math.cos(angle) * speed,
            'vy': math.sin(angle) * speed,
            'lifetime': max_lt,
            'max_lifetime': max_lt,
            'color': color,
            'radius': random.randint(2, 5),
        })


def update_particles(particles, dt):
    for p in particles:
        p['x'] += p['vx'] * dt
        p['y'] += p['vy'] * dt
        p['vx'] *= 0.91
        p['vy'] *= 0.91
        p['lifetime'] -= dt
    particles[:] = [p for p in particles if p['lifetime'] > 0]


def draw_particles(surface, particles):
    for p in particles:
        t = p['lifetime'] / p['max_lifetime']
        r = max(1, int(p['radius'] * t))
        c = tuple(int(ch * t) for ch in p['color'])
        pygame.draw.circle(surface, c, (int(p['x']), int(p['y'])), r)


# --- UI helpers ---

def draw_text_centered(surface, text, font, color, cy):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(SCREEN_W // 2, cy))
    surface.blit(surf, rect)


def draw_hud(surface, font_sm, score, lives):
    # semi-transparent panel at top
    panel = pygame.Surface((SCREEN_W, 36), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 150))
    surface.blit(panel, (0, 0))

    surface.blit(font_sm.render(f"Score: {score}", True, WHITE), (10, 8))

    lives_surf = font_sm.render(f"Lives: {lives}", True, CYAN)
    surface.blit(lives_surf, (SCREEN_W - lives_surf.get_width() - 10, 8))

    # progress bar towards victory score
    bar_w = 200
    bar_x = SCREEN_W // 2 - bar_w // 2
    bar_y = 11
    progress = min(score / VICTORY_SCORE, 1.0)
    pygame.draw.rect(surface, (50, 50, 70), (bar_x, bar_y, bar_w, 14), border_radius=4)
    if progress > 0:
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, int(bar_w * progress), 14), border_radius=4)
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, 14), 1, border_radius=4)


# --- Difficulty ---

def get_difficulty(elapsed):
    if elapsed < 20:
        return 2.0, 1.5
    if elapsed < 40:
        return 3.0, 1.2
    return 4.0, 0.9


# --- Game states ---

def run_menu(screen, clock, font_big, font_med, font_sm, stars):
    t = 0.0
    while True:
        dt = clock.tick(FPS) / 1000.0
        t += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        update_stars(stars, dt)
        screen.fill(DARK)
        draw_stars(screen, stars)

        # pulsing title
        pulse = int(190 + 65 * math.sin(t * 2.2))
        draw_text_centered(screen, "SPACE DEFENDER", font_big, (0, pulse, 255), 140)
        draw_text_centered(screen, "Destrua asteroides e alcance 500 pontos!", font_sm, GRAY, 197)

        # controls box with alpha background
        box_x, box_y, box_w, box_h = 230, 242, 340, 178
        box_surf = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        box_surf.fill((15, 15, 45, 190))
        screen.blit(box_surf, (box_x, box_y))
        pygame.draw.rect(screen, CYAN, (box_x, box_y, box_w, box_h), 2, border_radius=10)

        draw_text_centered(screen, "Controles", font_med, YELLOW, box_y + 28)
        controls = [
            ("← →",   "Mover nave"),
            ("SPACE",  "Atirar"),
            ("ESC",    "Sair"),
        ]
        for i, (key, action) in enumerate(controls):
            ky = box_y + 65 + i * 38
            screen.blit(font_sm.render(key,    True, YELLOW), (box_x + 30,  ky))
            screen.blit(font_sm.render(action, True, WHITE),  (box_x + 145, ky))

        # blinking prompt
        if int(t * 2) % 2 == 0:
            draw_text_centered(screen, "Pressione ENTER para jogar", font_med, GREEN, 465)

        pygame.display.flip()


def run_playing(screen, clock, font_big, font_med, font_sm, stars):
    player = Player(SCREEN_W, SCREEN_H)
    asteroids = []
    bullets = []
    particles = []
    score = 0
    elapsed = 0.0
    spawn_timer = 0.0
    flash_timer = 0.0

    while True:
        dt = clock.tick(FPS) / 1000.0
        elapsed += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return MENU, score

        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.update(dt)

        bullet = player.try_shoot(keys, dt)
        if bullet:
            bullets.append(bullet)

        base_speed, spawn_interval = get_difficulty(elapsed)
        spawn_timer -= dt
        if spawn_timer <= 0:
            asteroids.append(Asteroid(SCREEN_W, base_speed))
            spawn_timer = spawn_interval + random.uniform(-0.1, 0.1)

        for b in bullets:
            b.update(dt)
        for a in asteroids:
            a.update(dt)

        update_particles(particles, dt)

        # bullet × asteroid collision
        hit_bullets = set()
        hit_asteroids = set()
        for bi, b in enumerate(bullets):
            for ai, a in enumerate(asteroids):
                if a.collides_with_bullet(b):
                    hit_bullets.add(bi)
                    hit_asteroids.add(ai)
                    score += a.score_value()
                    spawn_explosion(particles, a.x, a.y, a.color)

        bullets   = [b for i, b in enumerate(bullets)   if i not in hit_bullets]
        asteroids = [a for i, a in enumerate(asteroids) if i not in hit_asteroids]

        # asteroid × player collision
        for a in asteroids[:]:
            if a.collides_with_player(player):
                if player.hit():
                    asteroids.remove(a)
                    flash_timer = 0.25

        # remove off-screen entities
        bullets   = [b for b in bullets   if not b.is_off_screen()]
        asteroids = [a for a in asteroids if not a.is_off_screen(SCREEN_H)]

        if player.lives <= 0:
            return GAME_OVER, score
        if score >= VICTORY_SCORE:
            return VICTORY, score

        # --- draw ---
        update_stars(stars, dt)
        screen.fill(DARK)
        draw_stars(screen, stars)

        for a in asteroids:
            a.draw(screen)
        for b in bullets:
            b.draw(screen)
        draw_particles(screen, particles)
        player.draw(screen)

        # red flash on player hit
        if flash_timer > 0:
            flash_timer -= dt
            alpha = int(110 * (flash_timer / 0.25))
            flash_surf = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
            flash_surf.fill((220, 0, 0, alpha))
            screen.blit(flash_surf, (0, 0))

        draw_hud(screen, font_sm, score, player.lives)
        pygame.display.flip()


def run_end_screen(screen, clock, font_big, font_med, font_sm, stars, state, score):
    if state == VICTORY:
        title, color, msg = "VITÓRIA!", GREEN, "Você destruiu todos os asteroides!"
    else:
        title, color, msg = "GAME OVER", RED, "Sua nave foi destruída..."

    t = 0.0
    while True:
        dt = clock.tick(FPS) / 1000.0
        t += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return MENU
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        update_stars(stars, dt)
        screen.fill(DARK)
        draw_stars(screen, stars)

        draw_text_centered(screen, title, font_big, color, 180)
        draw_text_centered(screen, msg, font_med, GRAY, 258)
        draw_text_centered(screen, f"Pontuação final: {score}", font_med, YELLOW, 308)

        if int(t * 2) % 2 == 0:
            draw_text_centered(screen, "ENTER — Voltar ao menu     ESC — Sair", font_sm, WHITE, 420)

        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Space Defender")
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 64, bold=True)
    font_med = pygame.font.SysFont("Arial", 28)
    font_sm  = pygame.font.SysFont("Arial", 22)

    stars = make_stars()
    state = MENU

    while True:
        if state == MENU:
            run_menu(screen, clock, font_big, font_med, font_sm, stars)
            state = PLAYING
        elif state == PLAYING:
            state, score = run_playing(screen, clock, font_big, font_med, font_sm, stars)
        else:
            state = run_end_screen(screen, clock, font_big, font_med, font_sm, stars, state, score)


if __name__ == "__main__":
    main()
