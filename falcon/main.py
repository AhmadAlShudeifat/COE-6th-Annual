import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Desert Sky Defender")
clock = pygame.time.Clock()

background = pygame.transform.scale(
    pygame.image.load("desert.jpg").convert(), (WIDTH, HEIGHT)
)
launcher_image = pygame.transform.scale(
    pygame.image.load("launcher.png").convert_alpha(), (90, 90)
)
falcon_right_image = pygame.transform.scale(
    pygame.image.load("falcon.png").convert_alpha(), (80, 55)
)
projectile_image = pygame.transform.scale(
    pygame.image.load("projectile.png").convert_alpha(), (16, 28)
)

font = pygame.font.Font(None, 36)

def falcon_image_for_movement(dx):
    return pygame.transform.flip(falcon_right_image, True, False) if dx < 0 else falcon_right_image

launcher_rect = launcher_image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))
falcon_rect = falcon_right_image.get_rect(center=(WIDTH // 2, 180))
falcon_image = falcon_right_image

projectiles = []
hits = 0
hit_goal = 10
time_limit = 60
start_time = pygame.time.get_ticks()
winner = None
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_SPACE and winner is None:
                projectile = projectile_image.get_rect(
                    midbottom=launcher_rect.midtop
                )
                projectiles.append(projectile)

    keys = pygame.key.get_pressed()

    if winner is None:
        if keys[pygame.K_LEFT]:
            launcher_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            launcher_rect.x += 5
        launcher_rect.clamp_ip(screen.get_rect())

        dx = 0
        if keys[pygame.K_a]:
            falcon_rect.x -= 5
            dx = -1
        if keys[pygame.K_d]:
            falcon_rect.x += 5
            dx = 1
        if keys[pygame.K_w]:
            falcon_rect.y -= 5
        if keys[pygame.K_s]:
            falcon_rect.y += 5

        if dx != 0:
            falcon_image = falcon_image_for_movement(dx)

        falcon_rect.clamp_ip(pygame.Rect(0, 0, WIDTH, 430))

        for projectile in projectiles[:]:
            projectile.y -= 8
            if projectile.bottom < 0:
                projectiles.remove(projectile)

        for projectile in projectiles[:]:
            if projectile.colliderect(falcon_rect):
                projectiles.remove(projectile)
                hits += 1
                if hits >= hit_goal:
                    winner = "Player 1 (launcher)"

        elapsed = (pygame.time.get_ticks() - start_time) / 1000
        if elapsed >= time_limit and winner is None:
            winner = "Player 2 (falcon)"

    else:
        elapsed = (pygame.time.get_ticks() - start_time) / 1000

    screen.blit(background, (0, 0))
    screen.blit(falcon_image, falcon_rect)
    screen.blit(launcher_image, launcher_rect)

    for projectile in projectiles:
        screen.blit(projectile_image, projectile)

    remaining = max(0, time_limit - int(elapsed))
    screen.blit(font.render(f"Hits: {hits}/{hit_goal}", True, (20, 20, 20)), (20, 20))
    screen.blit(font.render(f"Time: {remaining}", True, (20, 20, 20)), (20, 55))
    screen.blit(font.render("P1: arrows + Space   P2: WASD", True, (20, 20, 20)), (20, 90))

    if winner:
        message = font.render(f"{winner} wins! Press Esc to quit", True, (20, 20, 20))
        screen.blit(message, message.get_rect(center=(WIDTH // 2, 40)))

    pygame.display.flip()

pygame.quit()