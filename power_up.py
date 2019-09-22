

"""
"""


import config
import pygame
import random


class Power_Up(pygame.sprite.Sprite):


    def __init__(self, center):

        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(config.power_up_types)
        self.level = random.choices(config.power_up_levels, [20/30, 7/30, 3/30], k=1)[0]
        self.image = pygame.image.load( config.power_up_images[self.type + "_" + self.level]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = config.DIFFICULTY * random.randrange(3, 8)


    def update(self):

        self.rect.y += self.speedy
        if self.rect.top > config.HEIGHT:
            self.kill()
