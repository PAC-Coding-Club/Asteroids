import random
import asyncio
import pygame
import sys
import objects

pygame.init()
font = pygame.font.SysFont("Segoe UI", 35)


fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1024, 768))

players = pygame.sprite.Group()
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
player = objects.Player((screen.get_width() / 2, screen.get_height() / 2), players)

score = 0
score_for_life = 10000
lives = 3

max_lives = 5

invisible = fps * 5 # invincibility for 5 seconds
invincibility_seconds = 5

for i in range(random.randint(4, 6)):
    objects.Asteroid((random.randint(0, screen.get_width()), random.randint(0, screen.get_height())), 3, asteroids)


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if len(bullets.sprites()) < 4 and lives > 0:
                    objects.Bullet(player, bullets)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                objects.Asteroid(event.pos, 3, asteroids)

    keys_pressed = pygame.key.get_pressed()

    player.update(keys_pressed)
    bullets.update()
    asteroids.update()

    # Collisions
    for asteroid in asteroids:
        if invisible > 0:
            invisible -= 1
        elif invisible <= 0:
            invisible = 0
            if player.rect.colliderect(asteroid.rect):
                lives -= 1
                invisible = fps * invincibility_seconds

        for bullet in bullets:
            if asteroid.rect.colliderect(bullet.rect):
                bullet.kill()
                if asteroid.size == 3:
                    score += 250
                if asteroid.size == 2:
                    score += 100
                if asteroid.size == 1:
                    score += 25
                asteroid.split()

    if score > score_for_life and lives < max_lives + 1:
        score_for_life += 10000
        lives += 1

    screen.fill("black")  # fill the screen with black

    # Game Over
    if lives == 0:
        player.kill()
        dead_textsurface = font.render(f"YOU DIED", False, "red")  # create score surface
        screen.blit(dead_textsurface, (screen.get_width() / 2 - dead_textsurface.get_width() / 2, screen.get_height() / 2 - dead_textsurface.get_height() / 2))

    bullets.draw(screen)  # draw the sprites
    asteroids.draw(screen)
    players.draw(screen)

    textsurface = font.render(f"Score: {score}", False, "white")  # create score surface
    screen.blit(textsurface, (13, 0))  # draw the score surface

    # draw lives
    for i in range(lives):
        screen.blit(player.image_original, (i * 50 + 15, 60))

    pygame.display.update()  # update the screen

    asyncio.sleep(0)  # Required for creating a Web Version
    clock.tick(fps)  # Tick clock to set FPS

pygame.quit()
sys.exit()
