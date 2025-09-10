import math
import pygame
import random

# Initialize pygame
pygame.init()

# Frame size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particle Logic')
clock = pygame.time.Clock()

# Particle class
def random_velocity():
    return random.uniform(-2, 2), random.uniform(-2, 2)

class Particle:
    def __init__(self):
        self.x = random.randint(50, WIDTH-50)
        self.y = random.randint(50, HEIGHT-50)
        self.vx, self.vy = random_velocity()
        self.radius =10
        self.mass = 10.0
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Realistic wall bounce
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
    # Tangent vector
    tx = -ny
    ty = nx
    # Velocities along normal and tangent
    va_n = a.vx * nx + a.vy * ny
    vb_n = b.vx * nx + b.vy * ny
    va_t = a.vx * tx + a.vy * ty
    vb_t = b.vx * tx + b.vy * ty
    # Only swap normal components
    m1, m2 = a.mass, b.mass
    va_n_new = (va_n * (m1 - m2) + 2 * m2 * vb_n) / (m1 + m2)
    vb_n_new = (vb_n * (m2 - m1) + 2 * m1 * va_n) / (m1 + m2)
    # Update velocities
    a.vx = va_n_new * nx + va_t * tx
    a.vy = va_n_new * ny + va_t * ty
    b.vx = vb_n_new * nx + vb_t * tx
    b.vy = vb_n_new * ny + vb_t * ty

def handle_collisions_grid(particles, cell_size=40):
    grid = {}
    for idx, p in enumerate(particles):
        cell_x = int(p.x // cell_size)
        cell_y = int(p.y // cell_size)
        key = (cell_x, cell_y)
        if key not in grid:
            grid[key] = []
        grid[key].append(idx)
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
                                apply_elastic_impulse(a, b, restitution=1.0)
                            checked.add((i, j))

# Create 10 particles
particles = [Particle() for _ in range(20)]


    

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))  # Frame background
    for p in particles:
        p.move()
    handle_collisions_grid(particles, cell_size=40)
    for p in particles:
        p.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()