import pygame
import sys
import random
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
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
YELLOW  = (255, 220, 0)
CYAN    = (0, 200, 255)
RED     = (220, 60, 60)
GREEN   = (60, 220, 100)
GRAY    = (180, 180, 180)
DARK    = (15, 15, 30)


def draw_stars(surface, stars):
    for x, y, brightness in stars:
        pygame.draw.circle(surface, (brightness, brightness, brightness), (x, y), 1)


def make_stars(n=120):
    return [
        (random.randint(0, SCREEN_W), random.randint(0, SCREEN_H), random.randint(80, 220))
        for _ in range(n)
    ]


def draw_text_centered(surface, text, font, color, cy):
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(SCREEN_W // 2, cy))
    surface.blit(surf, rect)


def draw_hud(surface, font_sm, score, lives):
    score_surf = font_sm.render(f"Score: {score}", True, WHITE)
    surface.blit(score_surf, (10, 10))

    lives_surf = font_sm.render(f"Vidas: {lives}", True, CYAN)
    surface.blit(lives_surf, (SCREEN_W - lives_surf.get_width() - 10, 10))

    # progress bar towards victory score
    bar_w = 200
    bar_x = SCREEN_W // 2 - bar_w // 2
    bar_y = 8
    progress = min(score / VICTORY_SCORE, 1.0)
    pygame.draw.rect(surface, GRAY, (bar_x, bar_y, bar_w, 14), border_radius=4)
    if progress > 0:
        pygame.draw.rect(surface, GREEN, (bar_x, bar_y, int(bar_w * progress), 14), border_radius=4)
    pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, 14), 1, border_radius=4)


def get_difficulty(elapsed):
    if elapsed < 20:
        return 2.0, 1.5
    if elapsed < 40:
        return 3.0, 1.2
    return 4.0, 0.9


def run_menu(screen, clock, font_big, font_med, font_sm, stars):
    while True:
        dt = clock.tick(FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        screen.fill(DARK)
        draw_stars(screen, stars)

        draw_text_centered(screen, "SPACE DEFENDER", font_big, CYAN, 140)
        draw_text_centered(screen, "Destrua asteroides e alcance 500 pontos!", font_sm, GRAY, 195)

        # controls box
        box_x, box_y, box_w, box_h = 230, 240, 340, 180
        pygame.draw.rect(screen, (25, 25, 50), (box_x, box_y, box_w, box_h), border_radius=10)
        pygame.draw.rect(screen, CYAN, (box_x, box_y, box_w, box_h), 2, border_radius=10)

        draw_text_centered(screen, "Controles", font_med, YELLOW, box_y + 28)
        controls = [
            ("← →", "Mover nave"),
            ("SPACE", "Atirar"),
            ("ESC", "Sair"),
        ]
        for i, (key, action) in enumerate(controls):
            y = box_y + 65 + i * 38
            key_surf = font_sm.render(key, True, YELLOW)
            act_surf = font_sm.render(action, True, WHITE)
            screen.blit(key_surf, (box_x + 30, y))
            screen.blit(act_surf, (box_x + 145, y))

        draw_text_centered(screen, "Pressione ENTER para jogar", font_med, GREEN, 465)
        pygame.display.flip()


def run_playing(screen, clock, font_big, font_med, font_sm, stars):
    player = Player(SCREEN_W, SCREEN_H)
    asteroids = []
    bullets = []
    score = 0
    elapsed = 0.0
    spawn_timer = 0.0

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

        # bullet × asteroid collision
        hit_bullets = set()
        hit_asteroids = set()
        for bi, b in enumerate(bullets):
            for ai, a in enumerate(asteroids):
                if a.collides_with_bullet(b):
                    hit_bullets.add(bi)
                    hit_asteroids.add(ai)
                    score += a.score_value()

        bullets    = [b for i, b in enumerate(bullets)    if i not in hit_bullets]
        asteroids  = [a for i, a in enumerate(asteroids)  if i not in hit_asteroids]

        # asteroid × player collision
        for a in asteroids[:]:
            if a.collides_with_player(player):
                if player.hit():
                    asteroids.remove(a)

        # remove off-screen entities
        bullets   = [b for b in bullets   if not b.is_off_screen()]
        asteroids = [a for a in asteroids if not a.is_off_screen(SCREEN_H)]

        if player.lives <= 0:
            return GAME_OVER, score
        if score >= VICTORY_SCORE:
            return VICTORY, score

        # --- draw ---
        screen.fill(DARK)
        draw_stars(screen, stars)

        for a in asteroids:
            a.draw(screen)
        for b in bullets:
            b.draw(screen)
        player.draw(screen)

        draw_hud(screen, font_sm, score, player.lives)
        pygame.display.flip()


def run_end_screen(screen, clock, font_big, font_med, font_sm, stars, state, score):
    if state == VICTORY:
        title, color, msg = "VITÓRIA!", GREEN, "Você destruiu todos os asteroides!"
    else:
        title, color, msg = "GAME OVER", RED, "Sua nave foi destruída..."

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return MENU
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        screen.fill(DARK)
        draw_stars(screen, stars)

        draw_text_centered(screen, title, font_big, color, 180)
        draw_text_centered(screen, msg, font_med, GRAY, 255)
        draw_text_centered(screen, f"Pontuação final: {score}", font_med, YELLOW, 305)
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
