# Particle Simulation

A 2D particle simulation using Pygame with pairwise Newtonian gravity, optional gravity centers, and grid-based collision handling. The project is intended for experimenting with physics and performance tuning.

## Requirements
- Python 3.7+
- pygame

Install pygame:
```
pip install pygame
```

## Run
From the project folder:
```
python main.py
```

## Controls
- G : Toggle spatial grid overlay
- 1-5 : Set target FPS (30 / 60 / 120 / 240 / 600)
- R / T : Decrease / increase restitution (collision elasticity)
- Left click : Set a gravity center at the clicked position
- Shift + Left click : Add another gravity center
- Right click : Clear all gravity centers
- Close window or press window close button to quit

## What to experiment with
Open `main.py` and `particle_logic.py` to tune simulation parameters:

Important knobs (in `main.py`)
- `PARTICLE_NUM` — number of particles (try lower/higher values)
- `SUBSTEPS` — physics substeps per frame (1 is fastest)
- `G` — gravitational constant used by the spatial gravity routine
- `GRAVITY_RADIUS` — radius (pixels) within which particles attract each other
- `CELL_SIZE` (in `particle_logic.py`) — spatial grid cell size used for collisions and neighbor search

Particle parameters (in `particle_logic.py`)
- `Particle.radius` and `Particle.mass` — adjust to see different dynamics
- `random_velocity()` — change initial velocities

## Performance tips
- Lower `PARTICLE_NUM` and `SUBSTEPS` to increase FPS.
- Increase `CELL_SIZE` to reduce neighbors per cell (faster neighbor search, may affect collision accuracy).
- Reduce `GRAVITY_RADIUS` to limit O(N) neighbors per particle.
- For very large N consider implementing Barnes-Hut (quadtree) or using Numba/Cython for heavy loops.


