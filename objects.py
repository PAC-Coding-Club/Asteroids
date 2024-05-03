import math
import random
from copy import copy
import pygame


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, location, size, *groups: pygame.sprite.Group):
        super().__init__(*groups)

        self.speed = pygame.Vector2(1, 1).copy()
        self.speed.rotate_ip(random.randint(0, 360))
        self.position = pygame.Vector2(location).copy()

        self.size = size
        if self.size == 1:
            self.image = pygame.image.load("assests/asteroid1.png")
        elif self.size == 2:
            self.image = pygame.image.load("assests/asteroid2.png")
        elif self.size == 3:
            self.image = pygame.image.load("assests/asteroid3.png")

        self.image = pygame.transform.rotate(self.image, random.randint(0, 360))
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def update(self):
        self.position += self.speed
        self.rect.center = self.position

        # wrap around screen edges
        if self.position.x > 1024:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1024
        if self.position.y > 768:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 768

    def split(self):
        if self.size > 1:
            for i in range(2):
                Asteroid(self.position, self.size - 1, self.groups())
            self.kill()
        else:
            self.kill()


class Bullet(pygame.sprite.Sprite):

    def __init__(self, player, *groups: pygame.sprite.Group):
        super().__init__(*groups)
        self.image = pygame.image.load("assests/bullet.png")
        self.rect = self.image.get_rect()
        self.position = copy(player.position)
        self.rect.center = self.position
        self.timer = 0
        self.lifetime = 60 * 1.5

        bullet_speed = 6
        self.speed = pygame.Vector2(bullet_speed * math.cos(player.angle), bullet_speed * -math.sin(player.angle)) + player.speed

    def update(self, *groups: pygame.sprite.Group):
        if self.timer > self.lifetime:
            self.kill()
        else:
            self.timer += 1

        self.position += self.speed
        self.rect.center = self.position

        # wrap around screen edges
        if self.position.x > 1024:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1024
        if self.position.y > 768:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 768


class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups: pygame.sprite.Group):
        super().__init__(*groups)

        # Fixed Values
        self.max_speed = 3
        self.r_speed = 0.05
        self.acceleration = 0.08

        # Altered Values
        self.angle = 0
        self.speed = pygame.Vector2(0, 0)
        self.angle = 0
        self.position = pygame.Vector2(location)

        # Image and Rect
        self.image = pygame.image.load("assests/player.png")
        self.image_original = self.image.copy()
        self.image_thrust = pygame.image.load("assests/player_thrust.png") # to be changed to a different image w/ blaster on back
        self.rect = self.image.get_rect()

    def update(self, keys_pressed):

        # add or minus r_speed from angle
        if keys_pressed[pygame.K_LEFT]:
            self.angle += self.r_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.angle -= self.r_speed
        if keys_pressed[pygame.K_DOWN]:
            # add acceleration to speed when thrusting
            self.speed.x += self.acceleration * math.cos(self.angle)
            self.speed.y -= self.acceleration * math.sin(self.angle)  # minus because of inverted y-axis

            # rotate image according to angle and depending on whether is thrusting
            self.image = pygame.transform.rotate(self.image_thrust, math.degrees(self.angle))
        else:
            self.image = pygame.transform.rotate(self.image_original, math.degrees(self.angle))

        # Move the player by speed with max speed
        if self.speed.length() > self.max_speed:
            self.speed.scale_to_length(self.max_speed)
        self.position += self.speed

        # wrap position around edges of screen
        if self.position.x > 1024:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = 1024
        if self.position.y > 768:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = 768

        # update rect
        self.rect = self.image.get_rect(center=self.position)
