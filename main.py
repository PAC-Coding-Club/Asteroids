import pygame
import sys
import math
import objects

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 768))

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
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

    # continuous movement
    keys_pressed = pygame.key.get_pressed()

    sprites.update(keys_pressed)

    for bullet in bullets.sprites():
        if player.rect.colliderect(bullet.rect):
            print("collide")

    screen.fill("grey")
    sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
