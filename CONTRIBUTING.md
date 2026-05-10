# Contributing

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python main.py
   ```

## Project structure

- `main.py` — game loop, state machine, rendering pipeline
- `entities.py` — `Player`, `Asteroid`, and `Bullet` classes

## Guidelines

- Keep all visuals in `pygame.draw` calls — no external image assets
- Each entity manages its own drawing and collision logic
- Game states are self-contained functions in `main.py`; add new states by following the same pattern (`run_<state>` returning the next state)
- Difficulty scaling lives in `get_difficulty(elapsed)` — adjust thresholds there
