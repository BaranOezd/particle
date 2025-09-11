# Particle Simulation

This project simulates elastic and inelastic collisions between particles using Pygame. Particles bounce off walls and each other with realistic physics. The simulation uses a grid-based approach for efficient collision detection and supports interactive gravity.

## Features
- Realistic elastic/inelastic collisions (adjustable restitution)
- Wall bouncing
- Random particle colors
- Grid-based collision optimization
- Toggle grid overlay with 'G' key
- Interactive gravity: left-click to attract particles, right-click to clear
- Adjustable FPS: 1-5 keys (30, 60, 120, 240, 600)
- HUD overlay: FPS, kinetic energy, collision count, restitution

## Requirements
- Python 3.x
- pygame

## Installation
Install pygame if you don't have it:
```
pip install pygame
```

## Usage
Run the simulation:
```
python main.py
```

### Controls
- **G**: Toggle grid overlay
- **1/2/3/4/5**: Set target FPS (30, 60, 120, 240, 600)
- **R/T**: Decrease/increase restitution (inelastic/elastic collisions)
- **Left-click**: Set gravity target (particles attracted to point)
- **Right-click**: Clear gravity target

## Files
- `main.py`: Main loop and UI logic
- `particle_logic.py`: Particle physics and collision logic
