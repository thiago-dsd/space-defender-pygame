import pygame
import random
import math


class Player:
    WIDTH = 40
    HEIGHT = 30
    SPEED = 5
    SHOOT_COOLDOWN = 0.3
    INVINCIBLE_DURATION = 1.5

    def __init__(self, screen_w, screen_h):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.x = screen_w // 2
        self.y = screen_h - 60
        self.lives = 3
        self.shoot_timer = 0.0
        self.invincible_timer = 0.0
        self.visible = True
        self.blink_timer = 0.0

    def handle_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.x = max(self.WIDTH // 2, self.x - self.SPEED)
        if keys[pygame.K_RIGHT]:
            self.x = min(self.screen_w - self.WIDTH // 2, self.x + self.SPEED)

    def try_shoot(self, keys, dt):
        self.shoot_timer -= dt
        if keys[pygame.K_SPACE] and self.shoot_timer <= 0:
            self.shoot_timer = self.SHOOT_COOLDOWN
            return Bullet(self.x, self.y - self.HEIGHT // 2)
        return None

    def update(self, dt):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = 0.1
        else:
            self.visible = True

    def hit(self):
        if self.invincible_timer > 0:
            return False
        self.lives -= 1
        self.invincible_timer = self.INVINCIBLE_DURATION
        self.blink_timer = 0.1
        return True

    def get_rect(self):
        return pygame.Rect(
            self.x - self.WIDTH // 2,
            self.y - self.HEIGHT // 2,
            self.WIDTH,
            self.HEIGHT,
        )

    def draw(self, surface):
        if not self.visible:
            return
        x, y = self.x, self.y
        hw = self.WIDTH // 2
        hh = self.HEIGHT // 2

        # engine flame (flickers each frame)
        fh = random.randint(8, 18)
        flame_outer = [
            (x - 8, y + hh),
            (x + 8, y + hh),
            (x + 3, y + hh + fh // 2),
            (x, y + hh + fh),
            (x - 3, y + hh + fh // 2),
        ]
        flame_inner = [
            (x - 4, y + hh),
            (x + 4, y + hh),
            (x, y + hh + fh // 2),
        ]
        pygame.draw.polygon(surface, (255, 120, 0), flame_outer)
        pygame.draw.polygon(surface, (255, 230, 80), flame_inner)

        # ship: triangle body
        points = [
            (x, y - hh),
            (x - hw, y + hh),
            (x + hw, y + hh),
        ]
        pygame.draw.polygon(surface, (0, 180, 230), points)
        pygame.draw.polygon(surface, (100, 220, 255), points, 2)

        # cockpit
        pygame.draw.circle(surface, (180, 240, 255), (x, y - 2), 6)
        pygame.draw.circle(surface, (0, 140, 200), (x, y - 2), 4)

        # cannon barrel
        pygame.draw.rect(surface, (140, 140, 210), (x - 3, y - hh - 10, 6, 12))
        pygame.draw.rect(surface, (200, 200, 255), (x - 2, y - hh - 10, 4, 12))


class Asteroid:
    def __init__(self, screen_w, base_speed):
        self.radius = random.randint(15, 40)
        self.x = random.randint(self.radius, screen_w - self.radius)
        self.y = -self.radius
        self.speed = base_speed + random.uniform(0, 1.5)
        self.rotation = 0.0
        self.rot_speed = random.uniform(-60, 60)
        self.color = random.choice([
            (160, 82, 45), (139, 90, 43), (120, 100, 60), (150, 130, 80)
        ])
        self.highlight = tuple(min(255, c + 45) for c in self.color)
        self._build_shape()
        self._build_crater()

    def _build_shape(self):
        r = self.radius
        count = random.randint(7, 11)
        self.offsets = []
        for i in range(count):
            angle = 2 * math.pi * i / count
            dist = r * random.uniform(0.7, 1.0)
            self.offsets.append((math.cos(angle) * dist, math.sin(angle) * dist))

    def _build_crater(self):
        # crater offset that rotates with the body
        dist = self.radius * 0.28
        angle = random.uniform(0, 2 * math.pi)
        self.crater_off = (math.cos(angle) * dist, math.sin(angle) * dist)
        self.crater_r = max(3, self.radius // 4)
        self.crater_color = tuple(max(0, c - 35) for c in self.color)

    def update(self, dt):
        self.y += self.speed
        self.rotation += self.rot_speed * dt

    def is_off_screen(self, screen_h):
        return self.y - self.radius > screen_h

    def get_points(self):
        rad = math.radians(self.rotation)
        cos_r, sin_r = math.cos(rad), math.sin(rad)
        pts = []
        for ox, oy in self.offsets:
            rx = ox * cos_r - oy * sin_r + self.x
            ry = ox * sin_r + oy * cos_r + self.y
            pts.append((rx, ry))
        return pts

    def draw(self, surface):
        pts = self.get_points()
        pygame.draw.polygon(surface, self.color, pts)
        pygame.draw.polygon(surface, self.highlight, pts, 2)

        # rotating crater
        rad = math.radians(self.rotation)
        cos_r, sin_r = math.cos(rad), math.sin(rad)
        ox, oy = self.crater_off
        cx = ox * cos_r - oy * sin_r + self.x
        cy = ox * sin_r + oy * cos_r + self.y
        pygame.draw.circle(surface, self.crater_color, (int(cx), int(cy)), self.crater_r)

    def collides_with_bullet(self, bullet):
        dx = bullet.x - self.x
        dy = bullet.y - self.y
        return math.sqrt(dx * dx + dy * dy) < self.radius + bullet.RADIUS

    def collides_with_player(self, player):
        rect = player.get_rect()
        cx = max(rect.left, min(self.x, rect.right))
        cy = max(rect.top, min(self.y, rect.bottom))
        dx = self.x - cx
        dy = self.y - cy
        return math.sqrt(dx * dx + dy * dy) < self.radius

    def score_value(self):
        # smaller asteroids are worth more points
        if self.radius <= 20:
            return 30
        if self.radius <= 30:
            return 20
        return 10


class Bullet:
    SPEED = 600
    RADIUS = 4

    def __init__(self, x, y):
        self.x = x
        self.y = float(y)

    def update(self, dt):
        self.y -= self.SPEED * dt

    def is_off_screen(self):
        return self.y < -self.RADIUS

    def draw(self, surface):
        # elongated laser bolt
        pygame.draw.rect(surface, (255, 255, 100), (int(self.x) - 2, int(self.y) - 9, 4, 16))
        pygame.draw.rect(surface, (255, 255, 255), (int(self.x) - 1, int(self.y) - 9, 2, 16))
