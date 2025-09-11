import pygame
from particle_logic import Particle, handle_collisions_grid, draw_grid, WIDTH, HEIGHT, CELL_SIZE, get_total_kinetic_energy

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
    screen.fill((30, 30, 30))
    for _ in range(4):
        for p in particles:
            p.move(substeps=4)
        collision_count += handle_collisions_grid(particles, cell_size=CELL_SIZE)
    if show_grid_overlay:
        draw_grid(screen, cell=CELL_SIZE)
    for p in particles:
        p.draw(screen)
    # HUD overlay
    fps = clock.get_fps()
    ke = get_total_kinetic_energy(particles)
    hud_lines = [
        f"FPS: {fps:.1f} (Target: {target_fps})",
        f"Kinetic Energy: {ke:.2f}",
        f"Collisions: {collision_count}"
    ]
    for i, line in enumerate(hud_lines):
        hud_text = font.render(line, True, (200, 200, 50))
        screen.blit(hud_text, (10, 10 + 22 * i))
    pygame.display.flip()
    clock.tick(target_fps)

pygame.quit()
