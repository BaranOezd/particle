import math
import random
import pygame

WIDTH = 1200
HEIGHT = 800
CELL_SIZE = 40

# Particle class
def random_velocity():
    return random.uniform(-2, 2), random.uniform(-2, 2)

class Particle:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = random.randint(50, HEIGHT-50)
        self.vx, self.vy = (0.0,0.0)
        self.radius = 3
        self.mass = random.randint(5, 400)  # Random mass between 5 and 15
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
    def move(self, substeps=1):
        self.x += self.vx / substeps
        self.y += self.vy / substeps
        if self.x < self.radius:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x > WIDTH - self.radius:
            self.x = WIDTH - self.radius
            self.vx = -self.vx
        if self.y < self.radius:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y > HEIGHT - self.radius:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

def draw_grid(surface, cell=CELL_SIZE, color=(60, 60, 60)):
    for x in range(0, WIDTH, cell):
        pygame.draw.line(surface, color, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, cell):
        pygame.draw.line(surface, color, (0, y), (WIDTH, y), 1)

def circles_collide(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    rsum = a.radius + b.radius
    return dx*dx + dy*dy <= rsum * rsum

def resolve_overlap(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        dx, dy = 1e-6, 0.0
        dist = 1e-6
    rsum = a.radius + b.radius
    overlap = rsum - dist
    if overlap > 0:
        nx = dx / dist
        ny = dy / dist
        total = a.mass + b.mass
        a.x -= nx * overlap * (b.mass / total)
        a.y -= ny * overlap * (b.mass / total)
        b.x += nx * overlap * (a.mass / total)
        b.y += ny * overlap * (a.mass / total)

def apply_elastic_impulse(a, b, restitution=1.0):
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy)
    if dist == 0:
        dx, dy = 1e-6, 0.0
        dist = 1e-6
    nx = dx / dist
    ny = dy / dist
    tx = -ny
    ty = nx
    va_n = a.vx * nx + a.vy * ny
    vb_n = b.vx * nx + b.vy * ny
    va_t = a.vx * tx + a.vy * ty
    vb_t = b.vx * tx + b.vy * ty
    m1, m2 = a.mass, b.mass
    # Inelastic collision: restitution < 1
    va_n_new = (va_n * (m1 - m2) + 2 * m2 * vb_n) / (m1 + m2)
    vb_n_new = (vb_n * (m2 - m1) + 2 * m1 * va_n) / (m1 + m2)
    va_n_new *= restitution
    vb_n_new *= restitution
    a.vx = va_n_new * nx + va_t * tx
    a.vy = va_n_new * ny + va_t * ty
    b.vx = vb_n_new * nx + vb_t * tx
    b.vy = vb_n_new * ny + vb_t * ty

def build_spatial_grid(particles, cell_size=CELL_SIZE):
    """Build a mapping from grid cell -> list of particle indices."""
    grid = {}
    for idx, p in enumerate(particles):
        cell_x = int(p.x // cell_size)
        cell_y = int(p.y // cell_size)
        key = (cell_x, cell_y)
        grid.setdefault(key, []).append(idx)
    return grid

def apply_newtonian_gravity_spatial(particles, grid, G=0.2, gravity_radius=200.0, cell_size=CELL_SIZE, softening=1e-2):
    """
    Apply Newtonian gravity using the provided spatial grid.
    Each particle only considers neighbors within gravity_radius.
    This reduces complexity for large N.
    """
    radius_cells = max(1, int(math.ceil(gravity_radius / cell_size)))
    radius_sq = gravity_radius * gravity_radius
    n = len(particles)
    # accumulate accelerations first to avoid order dependencies
    ax = [0.0] * n
    ay = [0.0] * n
    for key, indices in grid.items():
        # iterate particles in this cell and nearby cells
        cx, cy = key
        neighbor_cells = []
        for dx_cell in range(-radius_cells, radius_cells + 1):
            for dy_cell in range(-radius_cells, radius_cells + 1):
                neighbor_cells.append((cx + dx_cell, cy + dy_cell))
        for i in indices:
            a = particles[i]
            for nkey in neighbor_cells:
                if nkey not in grid:
                    continue
                for j in grid[nkey]:
                    if i == j:
                        continue
                    b = particles[j]
                    dx = b.x - a.x
                    dy = b.y - a.y
                    dist_sq = dx * dx + dy * dy + softening
                    if dist_sq > radius_sq:
                        continue
                    inv_r = 1.0 / math.sqrt(dist_sq)
                    inv_r3 = inv_r / dist_sq
                    # acceleration on a due to b: G * m_b * r_vec / r^3
                    factor = G * b.mass * inv_r3
                    ax[i] += factor * dx
                    ay[i] += factor * dy
    # apply accelerations
    for i, p in enumerate(particles):
        p.vx += ax[i]
        p.vy += ay[i]

def handle_collisions_grid(particles, cell_size=40, restitution=1.0, grid=None):
    """
    Collision handling using spatial grid. If a grid is provided, reuse it
    (avoids building it twice per substep).
    """
    if grid is None:
        grid = {}
        for idx, p in enumerate(particles):
            cell_x = int(p.x // cell_size)
            cell_y = int(p.y // cell_size)
            key = (cell_x, cell_y)
            if key not in grid:
                grid[key] = []
            grid[key].append(idx)
    collision_count = 0
    checked = set()
    for key, indices in grid.items():
        neighbors = [key,
                     (key[0]+1, key[1]), (key[0]-1, key[1]),
                     (key[0], key[1]+1), (key[0], key[1]-1),
                     (key[0]+1, key[1]+1), (key[0]-1, key[1]-1),
                     (key[0]+1, key[1]-1), (key[0]-1, key[1]+1)]
        for nkey in neighbors:
            if nkey in grid:
                for i in indices:
                    for j in grid[nkey]:
                        if i < j and (i, j) not in checked:
                            a, b = particles[i], particles[j]
                            if circles_collide(a, b):
                                resolve_overlap(a, b)
                                apply_elastic_impulse(a, b, restitution)
                                checked.add((i, j))
                                collision_count += 1
    return collision_count

def get_total_kinetic_energy(particles):
    return sum(0.5 * p.mass * (p.vx**2 + p.vy**2) for p in particles)

def apply_newtonian_gravity(particles, G=0.2):
    # Each particle attracts every other particle
    for i, a in enumerate(particles):
        fx, fy = 0.0, 0.0
        for j, b in enumerate(particles):
            if i == j:
                continue
            dx = b.x - a.x
            dy = b.y - a.y
            dist_sq = dx*dx + dy*dy + 1e-6
            dist = math.sqrt(dist_sq)
            # Newtonian gravity: F = G * m1 * m2 / r^2
            force = G * a.mass * b.mass / dist_sq
            fx += force * dx / dist
            fy += force * dy / dist
        # Acceleration: a = F / m
        a.vx += fx / a.mass
        a.vy += fy / a.mass
