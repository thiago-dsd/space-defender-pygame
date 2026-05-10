# 🚀 Space Defender

> 2D space shooter built with Python and Pygame — university project.

Destroy asteroids, survive long enough to reach **150 points**, and defend your ship from being hit 3 times.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-00B140?style=flat)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=flat&logo=windows&logoColor=white)

---

## 🎮 Gameplay

| State        | Description                        |
|--------------|------------------------------------|
| 📋 Menu      | Title screen with controls listed  |
| ▶️ Playing   | Shoot asteroids, dodge collisions  |
| 🏆 Victory   | Reached 150 points                 |
| 💀 Game Over | Lost all 3 lives                   |

### 🕹️ Controls

| Key     | Action        |
|---------|---------------|
| `← →`   | Move ship     |
| `SPACE` | Shoot         |
| `ESC`   | Quit / Menu   |
| `ENTER` | Confirm       |

### ⭐ Scoring

| Asteroid    | Points |
|-------------|--------|
| 🪨 Small (≤20px) | 30 |
| 🪨 Medium (≤30px) | 20 |
| 🪨 Large (>30px)  | 10 |

---

## ⚙️ Requirements

- Python 3.11+
- pygame 2.x

```bash
pip install pygame
```

---

## ▶️ Running

```bash
python main.py
```

## 📦 Building (Windows .exe)

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name "SpaceDefender" main.py
```

The executable will be at `dist/SpaceDefender.exe`. Zip and submit.

---

## 🗂️ Project structure

```
atividade_pratica/
├── main.py       # game loop and state machine (MENU → PLAYING → GAME_OVER/VICTORY)
└── entities.py   # Player, Asteroid, Bullet classes
```

> No external assets — all visuals are drawn with `pygame.draw`.
