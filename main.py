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

    # continuous movement
    keys_pressed = pygame.key.get_pressed()

    player.update(keys_pressed)

    screen.fill("grey")
    pygame.draw.rect(screen, "green", player.rect)
    pygame.draw.line(screen, "black", player.rect.center, (player.rect.center[0] + 50 * math.cos(player.angle), player.rect.center[1] + 50 * math.sin(player.angle)))
    sprites.draw(screen)
    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()
