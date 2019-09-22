
"""
Sprite for the Player
"""


import logging
import pygame

import config

from bullet             import Bullet


log = logging.getLogger(__name__)


class Player(pygame.sprite.Sprite):


    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        initial_img = pygame.image.load(config.player_ship).convert_alpha()
        self.image = pygame.transform.scale(initial_img, (50, 38))
        self.image_mini = pygame.image.load(config.player_life).convert_alpha()
        self.rect  = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = config.WIDTH // 2
        self.rect.bottom = config.HEIGHT - 10

        self.speedx = 0
        self.accelx = 0
        self.maxspeedx = 15
        self.maxaccelx = 40
        self.incraccelx = 5 # accelx when keyboard pressed
        self.friction = 2 # must be < incraccel in this current logic

        self.shoot_bonus_counter = 0

        self.initial_shield = 200
        self.shield = self.initial_shield

        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

        self.shoot_delay = 120
        self.last_shoot = pygame.time.get_ticks()


    def update(self):

        # Acceleration reinitialization
        self.accelx = 0

        # Acceleration determination
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_q]:
            self.accelx = -self.incraccelx
        elif keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.accelx = self.incraccelx

        # Speed first determination
        self.speedx += self.accelx

        # Friction correction (can't move if not enough speed to beat friction)
        if self.speedx > 0 and self.speedx < self.friction \
            or self.speedx < 0 and self.speedx > - self.friction:
            self.speedx = 0

        # Speed determination
        # Limit the maximum speed (max / min)
        # +
        # Friction (lost of one unity (-1 / +1))
        if self.speedx > 0:
            self.speedx = min(self.maxspeedx, self.speedx - self.friction)
        elif self.speedx < 0:
            self.speedx = max(-self.maxspeedx, self.speedx + self.friction)

        # Position determination
        self.rect.x += self.speedx

        # Collision with borders
        if self.rect.right > config.WIDTH:
            self.rect.right = config.WIDTH
        elif self.rect.left < 0:
            self.rect.left = 0

        # Hiding the player when the ship was destroyed
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1500:
            self.hidden = False
            self.rect.centerx = config.WIDTH // 2
            self.rect.bottom = config.HEIGHT - 10


    def shoot(self, bullets):

        bullet = Bullet(self.rect.centerx, self.rect.top, self.speedx)
        bullets.add(bullet)

        if self.shoot_bonus_counter > 0:
            bullet2 = Bullet(self.rect.centerx - 10, self.rect.top, self.speedx, -1, 'red')
            bullet3 = Bullet(self.rect.centerx + 10, self.rect.top, self.speedx, 1, 'red')
            bullets.add(bullet2, bullet3)

            if self.shoot_bonus_counter > 4:
                bullet2 = Bullet(self.rect.centerx - 20, self.rect.top, self.speedx, -2, 'blue_cross')
                bullet3 = Bullet(self.rect.centerx + 20, self.rect.top, self.speedx, 2, 'blue_cross')
                log.info("Quintuple!")
                bullets.add(bullet2, bullet3)

                if self.shoot_bonus_counter > 8:
                    bullet2 = Bullet(self.rect.centerx - 30, self.rect.top, self.speedx, -3, 'red_ball')
                    bullet3 = Bullet(self.rect.centerx + 30, self.rect.top, self.speedx, 3, 'red_ball')
                    log.info("Septuple!")
                    bullets.add(bullet2, bullet3)

            self.shoot_bonus_counter -= 1



    def hide(self):

        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (config.WIDTH // 2, config.HEIGHT + 200) # out of screen
