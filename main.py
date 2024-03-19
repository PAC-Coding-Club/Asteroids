import pygame
import sys
import math
import objects

clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 768))

sprites = pygame.sprite.Group()
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
                player.fire()

    # continuous movement
    keys_pressed = pygame.key.get_pressed()

    player.update(keys_pressed)

    screen.fill("grey")
    sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
