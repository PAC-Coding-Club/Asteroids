import math
from copy import copy
import pygame
from pygame.sprite import Group as _Group


def rot_center(image, angle, center):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)

    return rotated_image, new_rect

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups: _Group):
        super().__init__(*groups)

        # Fixed Values
        self.max_speed = 3
        self.r_speed = 0.05
        self.acceleration = 0.08

        # Altered Values
        self.angle = 0
        self.angle_old = 0
        self.speed = pygame.Vector2(0, 0)
        self.angle = 0
        self.position = pygame.Vector2(location)

        # Image and Rect
        self.image = pygame.image.load("player6.png")
        self.image_original = self.image.copy()
        self.rect = self.image.get_rect()

    def update(self, keys_pressed):
        # copy angle
        self.angle_old = copy(self.angle)

        # Set speed by acceleration
        if keys_pressed[pygame.K_LEFT]:
            self.angle -= self.r_speed
        if keys_pressed[pygame.K_RIGHT]:
            self.angle += self.r_speed
        if keys_pressed[pygame.K_UP]:
            self.speed.x += self.acceleration * math.cos(self.angle)
            self.speed.y += self.acceleration * math.sin(self.angle)

        # Move the player by speed with max speed
        if self.speed.length() > self.max_speed:
            self.speed.scale_to_length(self.max_speed)
        self.position += self.speed

        # rotate image according to angle (rotate func is opposite to unit circle)
        self.image, self.rect = rot_center(self.image_original, -math.degrees(self.angle), self.position)

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
        self.rect.center = self.position
    def fire(self):
        print("fired bullet")
