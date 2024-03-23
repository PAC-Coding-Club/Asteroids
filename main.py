import pygame
import sys
import objects

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 768))

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
player = objects.Player((200, 200), sprites)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                if len(bullets.sprites()) >= 4:
                    bullets.sprites()[0].kill()
                objects.Bullet(player, [sprites, bullets])
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                objects.Asteroid(event.pos, 3, [sprites, asteroids])

    # continuous movement
    keys_pressed = pygame.key.get_pressed()

    bullets.update(asteroids)
    player.update(keys_pressed)
    asteroids.update()

    screen.fill("black")
    sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
