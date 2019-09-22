

"""
"""


import config
import pygame


class Bullet(pygame.sprite.Sprite):


    def __init__(self, x, y, speedx, speedshift=0, color='green'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(config.laser_images[color]).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.bottom = y # in front of the player
        self.rect.centerx = x
        self.speedy = -10
        self.speedx = - speedx // 6 + speedshift
        self.rotate()


    def rotate(self):
        self.rot = - self.speedx * 3
        old_center = self.rect.center
        self.image = pygame.transform.rotate(self.image, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = old_center


    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # kill it after the exit of the screen
        if self.rect.bottom < 0:
            self.kill()
