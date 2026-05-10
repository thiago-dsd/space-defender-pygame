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
        # ship: triangle body
        points = [
            (x, y - self.HEIGHT // 2),
            (x - self.WIDTH // 2, y + self.HEIGHT // 2),
            (x + self.WIDTH // 2, y + self.HEIGHT // 2),
        ]
        pygame.draw.polygon(surface, (0, 200, 255), points)
        pygame.draw.polygon(surface, (255, 255, 255), points, 2)
        # cannon barrel
        pygame.draw.rect(surface, (180, 180, 255), (x - 3, y - self.HEIGHT // 2 - 8, 6, 10))


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
        self._build_shape()

    def _build_shape(self):
        r = self.radius
        count = random.randint(7, 11)
        self.offsets = []
        for i in range(count):
            angle = 2 * math.pi * i / count
            dist = r * random.uniform(0.7, 1.0)
            self.offsets.append((math.cos(angle) * dist, math.sin(angle) * dist))

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
        pygame.draw.polygon(surface, (220, 200, 150), pts, 2)

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
        pygame.draw.circle(surface, (255, 255, 100), (int(self.x), int(self.y)), self.RADIUS)
        pygame.draw.circle(surface, (255, 200, 0), (int(self.x), int(self.y)), self.RADIUS - 1)
