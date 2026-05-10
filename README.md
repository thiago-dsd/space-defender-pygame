# Space Defender

2D space shooter built with Python and Pygame — university project.

Destroy asteroids, survive long enough to reach **500 points**, and defend your ship from being hit 3 times.

---

## Gameplay

| State     | Description                          |
|-----------|--------------------------------------|
| Menu      | Title screen with controls listed    |
| Playing   | Shoot asteroids, dodge collisions    |
| Victory   | Reached 500 points                   |
| Game Over | Lost all 3 lives                     |

### Controls

| Key       | Action      |
|-----------|-------------|
| `← →`     | Move ship   |
| `SPACE`   | Shoot       |
| `ESC`     | Quit / Menu |
| `ENTER`   | Confirm     |

### Scoring

| Asteroid size | Points |
|---------------|--------|
| Small (≤20px) | 30     |
| Medium (≤30px)| 20     |
| Large (>30px) | 10     |

---

## Requirements

- Python 3.11+
- pygame 2.x

```
pip install pygame
```

## Running

```
python main.py
```

## Building (Windows .exe)

```
pip install pyinstaller
pyinstaller --onefile main.py
```

The executable will be at `dist/main.exe`. Zip and submit.

---

## Project structure

```
space_defender/
├── main.py       # game loop and state machine (MENU → PLAYING → GAME_OVER/VICTORY)
└── entities.py   # Player, Asteroid, Bullet classes
```

No external assets — all visuals are drawn with `pygame.draw`.
