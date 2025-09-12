import pygame
from particle_logic import (
    Particle, handle_collisions_grid, draw_grid, WIDTH, HEIGHT, CELL_SIZE,
    get_total_kinetic_energy, apply_newtonian_gravity_spatial, build_spatial_grid
)

PARTICLE_NUM = 100         # try hundreds; tune as needed
SUBSTEPS = 1               # fewer substeps improves throughput
GRAVITY_RADIUS = 220.0     # only consider neighbors within this radius
G = 0.02                   # tune gravitational constant (smaller for larger N)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particles')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

particles = [Particle() for _ in range(PARTICLE_NUM)]
show_grid_overlay = True
target_fps = 60
collision_count = 0
restitution = 0.4  # 1.0 = perfectly elastic, <1.0 = inelastic
gravity_targets = []  # List of gravity centers

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                show_grid_overlay = not show_grid_overlay
            elif event.key == pygame.K_1:
                target_fps = 30
            elif event.key == pygame.K_2:
                target_fps = 60
            elif event.key == pygame.K_3:
                target_fps = 120
            elif event.key == pygame.K_4:
                target_fps = 240
            elif event.key == pygame.K_5:
                target_fps = 600
            elif event.key == pygame.K_r:
                restitution = max(0.0, min(1.0, restitution - 0.1))
            elif event.key == pygame.K_t:
                restitution = max(0.0, min(1.0, restitution + 0.1))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mods = pygame.key.get_mods()
                if mods & pygame.KMOD_SHIFT:
                    gravity_targets.append(event.pos)  # Add new center
                else:
                    gravity_targets = [event.pos]  # Set single center
            elif event.button == 3:  # Right click
                gravity_targets = []  # Clear all centers
    screen.fill((30, 30, 30))
    for _ in range(SUBSTEPS):
        # build grid once per substep and reuse for gravity + collisions
        grid = build_spatial_grid(particles, cell_size=CELL_SIZE)
        # apply gravity only from nearby neighbors
        if len(particles) > 1:
            apply_newtonian_gravity_spatial(particles, grid, G=G, gravity_radius=GRAVITY_RADIUS, cell_size=CELL_SIZE)
        # optional gravity centers (kept simple)
        for target in gravity_targets:
            for p in particles:
                dx = target[0] - p.x
                dy = target[1] - p.y
                dist = (dx * dx + dy * dy) ** 0.5 + 1e-6
                strength = 0.015
                gx = strength * dx / dist
                gy = strength * dy / dist
                p.vx += gx
                p.vy += gy
        for p in particles:
            p.move(substeps=SUBSTEPS)
        # reuse grid for collision detection to avoid rebuilding
        collision_count += handle_collisions_grid(particles, cell_size=CELL_SIZE, restitution=restitution, grid=grid)
    if show_grid_overlay:
        draw_grid(screen, cell=CELL_SIZE)
    for p in particles:
        p.draw(screen)
    # Draw gravity targets
    for target in gravity_targets:
        pygame.draw.circle(screen, (255, 220, 80), target, 8)
    # HUD overlay
    fps = clock.get_fps()
    ke = get_total_kinetic_energy(particles)
    hud_lines = [
        f"FPS: {fps:.1f} (Target: {target_fps})",
        f"Kinetic Energy: {ke:.2f}",
        f"Collisions: {collision_count}",
        f"Restitution: {restitution:.2f} (R/T to change)",
        f"Gravity Centers: {len(gravity_targets)} (Shift+LClick to add)"
    ]
    for i, line in enumerate(hud_lines):
        hud_text = font.render(line, True, (200, 200, 50))
        screen.blit(hud_text, (10, 10 + 22 * i))
    pygame.display.flip()
    clock.tick(target_fps)

pygame.quit()
