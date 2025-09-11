import pygame
from particle_logic import Particle, handle_collisions_grid, draw_grid, WIDTH, HEIGHT, CELL_SIZE, get_total_kinetic_energy, apply_gravity_toward

PARTICLE_NUM = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particle Logic')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

particles = [Particle() for _ in range(PARTICLE_NUM)]
show_grid_overlay = True
target_fps = 60
collision_count = 0
gravity_target = None
restitution = 1.0  # 1.0 = perfectly elastic, <1.0 = inelastic

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
                gravity_target = event.pos
            elif event.button == 3:  # Right click
                gravity_target = None
    screen.fill((30, 30, 30))
    for _ in range(4):
        if gravity_target:
            apply_gravity_toward(particles, gravity_target, strength=0.03)
        for p in particles:
            p.move(substeps=4)
        collision_count += handle_collisions_grid(particles, cell_size=CELL_SIZE, restitution=restitution)
    if show_grid_overlay:
        draw_grid(screen, cell=CELL_SIZE)
    for p in particles:
        p.draw(screen)
    # Draw gravity target
    if gravity_target:
        pygame.draw.circle(screen, (255, 220, 80), gravity_target, 8)
    # HUD overlay
    fps = clock.get_fps()
    ke = get_total_kinetic_energy(particles)
    hud_lines = [
        f"FPS: {fps:.1f} (Target: {target_fps})",
        f"Kinetic Energy: {ke:.2f}",
        f"Collisions: {collision_count}",
        f"Restitution: {restitution:.2f} (R/T to change)"
    ]
    for i, line in enumerate(hud_lines):
        hud_text = font.render(line, True, (200, 200, 50))
        screen.blit(hud_text, (10, 10 + 22 * i))
    pygame.display.flip()
    clock.tick(target_fps)

pygame.quit()
