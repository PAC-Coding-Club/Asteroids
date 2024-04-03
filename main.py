import pygame
import sys
import objects

pygame.init()
font = pygame.font.SysFont("Segoe UI", 35)

fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 768))

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
player = objects.Player((200, 200), sprites)

score = 0
lives = 1


def draw_hit_boxes():
    pygame.draw.rect(screen, "red", player.rect, 1)
    for bullet in bullets:
        pygame.draw.rect(screen, "red", bullet.rect, 1)
    for asteroid in asteroids:
        pygame.draw.rect(screen, "green", asteroid.rect, 1)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if len(bullets.sprites()) < 4:
                    objects.Bullet(player, [sprites, bullets])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                objects.Asteroid(event.pos, 3, [sprites, asteroids])

    keys_pressed = pygame.key.get_pressed()

    bullets.update(asteroids)
    player.update(keys_pressed, asteroids)
    asteroids.update()

    screen.fill("black")
    sprites.draw(screen)
    textsurface = font.render(f"Score: {score}", False, "white")
    screen.blit(textsurface, (10, 10))

    draw_hit_boxes()
    pygame.display.update()

    clock.tick(fps)

pygame.quit()
sys.exit()
