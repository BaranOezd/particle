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
        self.radius = 30
        self.mass = float(self.radius)
        self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Bounce off walls
        if self.x < self.radius or self.x > WIDTH - self.radius:
            self.vx *= -1
        if self.y < self.radius or self.y > HEIGHT - self.radius:
            self.vy *= -1
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
    rvx = a.vx - b.vx
    rvy = a.vy - b.vy
    vel_along_normal = rvx * nx + rvy * ny
    if vel_along_normal > 0:
        return
    invA = 1.0 / a.mass
    invB = 1.0 / b.mass
    j = -(1.0 + restitution) * vel_along_normal
    j /= (invA + invB)
    impulse_x = j * nx
    impulse_y = j * ny
    a.vx += impulse_x * invA
    a.vy += impulse_y * invA
    b.vx -= impulse_x * invB
    b.vy -= impulse_y * invB

def handle_collisions(particles):
    n = len(particles)
    for i in range(n):
        for j in range(i + 1, n):
            a = particles[i]
            b = particles[j]
            if circles_collide(a, b):
                resolve_overlap(a, b)
                apply_elastic_impulse(a, b, restitution=1.0)

# Create 10 particles
particles = [Particle() for _ in range(10)]


    

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((30, 30, 30))  # Frame background
    for p in particles:
        p.move()
    handle_collisions(particles)
    for p in particles:
        p.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()