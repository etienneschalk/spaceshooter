

"""
Pygame's Space Shooter
-------------


By etsch,
Following the great kidscancode's youtube tutorial "Pygame Shmup"


Art
    Visual
        - All sprites are from Kenny's SpaceShooterRedux pack
        - Background image: https://imgur.com/bHiPMju
    Audio
        - Sound effects made with
        - Background music by last 2018's me, using FL Studio and Synth1

"""


import logging
import os
import pygame
import random

from enum                   import Enum

from game                   import Game


"""
MEMO
Idea : an plane shooting up oil barrels

Creating sounds effects:
https://www.bfxr.net/

Splits les gros asteroids en petits !


Mobs Bonus :
- Bullet transpercant : 3 hits de meteore avant de disparaitre
- Triple bullet (2 sur le coté)
- Ultra Speed (limited time) : spawns looots of buulets
- Ammo : give back ammo

Faille : on peut rester tranquille à l'abri en shootant
toujours au meme endroit. faire spawner des meteroids pres de la pos du joueur ?
"""

log = logging.getLogger(__name__)


def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S') #filename=...
    log.info("Game started")
    game = Game()
    game.run()
    log.info("Game finished")


if __name__ == "__main__":
    main()
