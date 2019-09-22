

"""
"""


import config
import pygame
import random


class Mob(pygame.sprite.Sprite):


    meteor_images = [pygame.image.load(meteor_filename) for meteor_filename in config.meteor_filenames]


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.initial_image = random.choice(self.meteor_images).convert_alpha()
        self.image = self.initial_image.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85) // 2
        self.rot = 0
        self.last_update = pygame.time.get_ticks()
        self.randomize_movement()


    def randomize_movement(self):
        self.rect.x = random.randrange(0, config.WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = config.DIFFICULTY * random.randrange(1, 12)
        self.speedx = config.DIFFICULTY * config.DIFFICULTY * random.randrange(-2, 2)
        self.rot_speed = config.DIFFICULTY * random.randrange(-8, 8)


    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.initial_image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > config.HEIGHT + 10 \
            or self.rect.left < -25 \
            or self.rect.right > config.WIDTH + 25:
            self.randomize_movement() # let's teleport it
