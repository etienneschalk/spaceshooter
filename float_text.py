

"""
Floating text, vanishing after its lifetime
Used to show points get or shield restauration to the player
"""


import pygame


class Float_Text():


    def __init__(self, text, lifetime, x, y):

        self.text = text
        self.lifetime = lifetime
        self.x = x
        self.y = y


    def update(self, decrease_lifetime, depl):

        self.lifetime -= decrease_lifetime
        self.y -= depl
