import pygame
from particle_logic import Particle, handle_collisions_grid, draw_grid, WIDTH, HEIGHT, CELL_SIZE

PARTICLE_NUM = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Particle Logic')
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

particles = [Particle() for _ in range(PARTICLE_NUM)]
show_grid_overlay = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_g:
                show_grid_overlay = not show_grid_overlay

    screen.fill((30, 30, 30))
    for p in particles:
        p.move()
        handle_collisions_grid(particles, cell_size=CELL_SIZE)
    if show_grid_overlay:
        draw_grid(screen, cell=CELL_SIZE)
    for p in particles:
        p.draw(screen)
    pygame.display.flip()
    # Draw FPS
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {fps:.1f}", True, (200, 200, 50))
    screen.blit(fps_text, (10, 10))
    clock.tick(60)
pygame.quit()
