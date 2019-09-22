

"""
Sound handler for all sounds needed in the game
"""


import config
import pygame
import random


class Sound_Handler():


    def __init__(self):

        l1   = pygame.mixer.Sound(config.l1)
        l2   = pygame.mixer.Sound(config.l2)
        l3   = pygame.mixer.Sound(config.l3)
        l4   = pygame.mixer.Sound(config.l4)
        e1   = pygame.mixer.Sound(config.e1)
        e2   = pygame.mixer.Sound(config.e2)
        e3   = pygame.mixer.Sound(config.e3)
        ep   = pygame.mixer.Sound(config.ep)
        pc2  = pygame.mixer.Sound(config.pc2)
        p6   = pygame.mixer.Sound(config.p6)

        self.sounds =  {
            "laser": [l1, l2, l3, l4],
            "explosion": [e1, e3],
            "player_hit": [e2],
            "player_death": [ep],
            "shield": [pc2],
            "bolt": [p6]
        }

        for s in self.sounds["laser"]:
            s.set_volume(0.15)

        for s in self.sounds["explosion"]:
            s.set_volume(0.2)

        for s in self.sounds["player_death"]:
            s.set_volume(0.2)

        for s in self.sounds["player_hit"]:
            s.set_volume(0.2)

        for s in self.sounds["bolt"]:
            s.set_volume(0.5)


    def play(self, name):
        random.choice(self.sounds[name]).play()
