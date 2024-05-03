import random
import asyncio
import pygame
import sys
import objects

pygame.init()
font = pygame.font.SysFont("Segoe UI", 35)

fps = 60

class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((1024, 768))

        self.sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.player = objects.Player((self.screen.get_width() / 2, self.screen.get_height() / 2), self.sprites)

        self.score = 0
        self.score_for_life = 10000
        self.lives = 3

        self.max_lives = 5

        self.invincible = fps * 5  # invincibility for 5 seconds
        self.invincibility_seconds = 5

        for i in range(random.randint(4, 6)):
            objects.Asteroid((random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height())), 3, [self.sprites, self.asteroids])

    async def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if len(self.bullets.sprites()) < 4:
                            objects.Bullet(self.player, [self.sprites, self.bullets])
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        objects.Asteroid(event.pos, 3, [self.sprites, self.asteroids])

            keys_pressed = pygame.key.get_pressed()

            self.player.update(keys_pressed)
            self.bullets.update()
            self.asteroids.update()

            # Collisions
            for asteroid in self.asteroids:
                if self.invincible > 0:
                    self.invincible -= 1
                elif self.invincible <= 0:
                    self.invincible = 0
                    if self.player.rect.colliderect(asteroid.rect):
                        self.lives -= 1
                        invincible = fps * self.invincibility_seconds

                for bullet in self.bullets:
                    if asteroid.rect.colliderect(bullet.rect):
                        bullet.kill()
                        if asteroid.size == 3:
                            self.score += 250
                        if asteroid.size == 2:
                            self.score += 100
                        if asteroid.size == 1:
                            self.score += 25
                        asteroid.split()

            if self.score > self.score_for_life and self.lives < self.max_lives + 1:
                self.score_for_life += 10000
                self.lives += 1

            self.screen.fill("black")  # fill the screen with black

            # Game Over
            if self.lives == 0:
                self.player.kill()
                dead_textsurface = font.render(f"YOU DIED", False, "red")  # create score surface
                self.screen.blit(dead_textsurface, (self.screen.get_width() / 2 - dead_textsurface.get_width() / 2, self.screen.get_height() / 2 - dead_textsurface.get_height() / 2))

            self.sprites.draw(self.screen)  # draw the sprites
            textsurface = font.render(f"Score: {self.score}", False, "white")  # create score surface
            self.screen.blit(textsurface, (13, 0))  # draw the score surface

            # draw lives
            for i in range(self.lives):
                self.screen.blit(self.player.image_original, (i * 50 + 15, 60))

            pygame.display.update()  # update the screen

            await asyncio.sleep(0)  # Required for creating a Web Version
            self.clock.tick(fps)  # Tick clock to set FPS


asyncio.run(Game().run())
