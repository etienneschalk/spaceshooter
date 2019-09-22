

"""
Moving background
"""


import pygame

import config


class Background(pygame.sprite.Sprite):


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(config.background).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = 0, 0
        self.moving_speed = 9


    def update(self):
        self.rect.top = (self.rect.top + self.moving_speed) % self.rect.h
