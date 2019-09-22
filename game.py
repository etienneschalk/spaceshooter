

"""
Space Shooter Game
"""


import logging
import pygame
import random

import config

from background             import Background
from color                  import Color
from explosion              import Explosion
from float_text             import Float_Text
from mob                    import Mob
from player                 import Player
from power_up               import Power_Up
from sound_handler          import Sound_Handler


log = logging.getLogger(__name__)


class Game:


    # initialize pygame and create window
    def __init__(self):

        # sound buffer size decrease
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Space Shooter")
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.background = Background()

        self.init_explosion_images()

        self.score = 0
        self.power_up_rate = 0.9 # default value: 0.9

        # Float_Texts
        self.score_textes = []
        self.shield_bonus_textes = []

        # Sound init
        self.sound_handler = Sound_Handler()
        self.sound_laser = self.sound_handler.sounds["laser"][1]
        pygame.mixer.music.load(config.background_music)
        pygame.mixer.music.play(loops=-1)

        # Loop continuing conditions
        self.running = True
        self.gameover = True

        # Hiding cursor
        pygame.mouse.set_visible(False)


    def init(self):

        self.sprites = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()

        for i in range(config.NB_MOBS):
            new_mob = Mob()
            new_mob.add(self.mobs, self.sprites)

        self.player = Player()
        self.sprites.add(self.player)

        self.score = 0
        self.gameover = False


    def init_explosion_images(self):

        self.explosion_anim = {}
        self.explosion_anim['lg'] = []
        self.explosion_anim['sm'] = []
        self.explosion_anim['player'] = []
        for i in range(9):
            img = pygame.image.load(config.regular_explosion_filenames[i]).convert_alpha()
            img_lg = pygame.transform.scale(img, (75, 75))
            self.explosion_anim['lg'].append(img_lg)
            img_sm = pygame.transform.scale(img, (32, 32))
            self.explosion_anim['sm'].append(img_sm)
            img_player = pygame.image.load(config.sonic_explosion_filenames[i]).convert_alpha()
            self.explosion_anim['player'].append(img_player)


    def draw_text(self, text, size, x, y, color):

        font = pygame.font.Font(config.font_name, size)
        text_surface = font.render(text, True, color) # antialiazed
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def draw_shield_bar(self):

        x = 10
        y = 10
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = (self.player.shield * 100) // self.player.initial_shield
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(self.screen, Color.GREEN.value, fill_rect)
        pygame.draw.rect(self.screen, Color.WHITE.value, outline_rect, 3)


    def draw_lives(self):

        for i in range(self.player.lives):
            img_rect = self.player.image_mini.get_rect()
            img_rect.x = config.WIDTH + (i - self.player.lives) * 40
            img_rect.y = 5
            self.screen.blit(self.player.image_mini, img_rect)


    def show_gameover_screen(self):

        waiting = True
        quitting = False

        while waiting:
            self.clock.tick(config.FPS)
            self.background.update()
            self.screen.blit(self.background.image, self.background.rect)
            self.screen.blit(self.background.image, (self.background.rect.x, self.background.rect.y - self.background.rect.h))
            self.draw_text("Space Shooter", 44, config.WIDTH//2, config.HEIGHT//4 - 30, Color.WHITE.value)
            self.draw_text("--- Commands ---", 14, config.WIDTH//2, (config.HEIGHT*2)//4 - 30,Color.WHITE.value)
            self.draw_text("[QD] or arrow keys to move", 14, config.WIDTH//2, (config.HEIGHT*2)//4 + 30 - 30,Color.WHITE.value)
            self.draw_text("[Space] to fire", 14, config.WIDTH//2, (config.HEIGHT*2)//4 + 50 - 30,Color.WHITE.value)
            self.draw_text("[Esc] to quit game", 14, config.WIDTH//2, (config.HEIGHT*2)//4 + 70 - 30,Color.WHITE.value)
            self.draw_text("Press [Enter] to play", 22, config.WIDTH//2, (config.HEIGHT*3)//4 + 70 - 30,Color.WHITE.value)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    quitting = True
                elif event.type == pygame.KEYDOWN:
                    log.info("[waiting menu] ["+str(event)+"] pressed")
                    if (event.key == pygame.K_ESCAPE):
                        self.running = False
                        quitting = True
                    if event.key == pygame.K_RETURN:
                        waiting = False
                        self.sound_handler.play('bolt')

            if quitting:
                waiting = False
                log.info("Exiting the game over waiting loop loop")


    def process_inputs(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.player.last_shoot > self.player.shoot_delay and not self.player.hidden:
                self.player.last_shoot = now
                self.player.shoot(self.bullets)
                self.sprites.add(self.bullets)
                self.sound_handler.play("laser")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                log.info("["+str(event)+"] pressed")
                if (event.key == pygame.K_ESCAPE):
                    self.gameover = True

    def update(self):

        self.background.update()
        self.sprites.update()

        # list of mobs collided with player ; mobs are deleted
        mob_hits_with_player = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_circle)

        for mob_hit in mob_hits_with_player:
            self.sound_handler.play("player_hit")
            self.player.shield -= mob_hit.radius*2
            expl = Explosion(self.explosion_anim, mob_hit.rect.center,'sm')
            self.sprites.add(expl)
            new_mob = Mob()
            new_mob.add(self.mobs, self.sprites)
            if self.player.shield < 0:
                self.sound_handler.play("player_death")
                self.death_explosion = Explosion(self.explosion_anim, self.player.rect.center, 'player')
                self.sprites.add(self.death_explosion)
                self.player.hide()
                self.player.lives -= 1
                self.player.shield = self.player.initial_shield

        # check if player died
        if self.player.lives == 0 and not self.death_explosion.alive():
            self.gameover = True
            log.info("Game Over!")
            log.info("Score: " + str(self.score))

        # list of mobs collided with the bullets ; both are deleted
        mob_hits_with_bullets = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)

        for mob_hit in mob_hits_with_bullets:
            self.sound_handler.play("explosion")
            points_gained = 60 - mob_hit.radius
            self.score += points_gained
            log.info("Hit Radius: " + str(mob_hit.radius))
            self.score_textes.append(Float_Text(str(points_gained), 60, mob_hit.rect.midtop[0], mob_hit.rect.midtop[1] - 10))
            expl = Explosion(self.explosion_anim, mob_hit.rect.center,'lg')
            self.sprites.add(expl)
            new_mob = Mob() # respawn a new mob
            new_mob.add(self.mobs, self.sprites)
            if random.random() > self.power_up_rate: # 90%
                power = Power_Up(mob_hit.rect.center)
                power.add(self.sprites, self.power_ups)

        # list of power_ups collided with player ; power_ups are deleted
        power_up_hits_with_player = pygame.sprite.spritecollide(self.player, self.power_ups, True)

        for pu_hit in power_up_hits_with_player:
            level = pu_hit.level
            if pu_hit.type == 'shield':
                self.sound_handler.play("shield")
                bonus = 1 if level == 'bronze' else 3 if level == 'silver' else 9
                bonus *= self.player.initial_shield // random.randrange(12,30) # 20 / 40 / 60 %
                self.player.shield +=  bonus
                self.player.shield = self.player.initial_shield if self.player.shield > self.player.initial_shield else self.player.shield
                self.shield_bonus_textes.append(Float_Text(str(bonus), 60, pu_hit.rect.midtop[0], pu_hit.rect.midtop[1] - 10))
            elif pu_hit.type == 'bolt':
                self.sound_handler.play("bolt")
                self.player.shoot_bonus_counter += 3 * (1 if level == 'bronze' else 2 if level == 'silver' else 4)

        # moving floating text about points got from destroying mobs
        self.score_textes = list(filter(lambda x: x.lifetime > 0, self.score_textes))
        for s in self.score_textes: s.update(2, 2)

        # moving floating text about shield bonuses
        self.shield_bonus_textes = list(filter(lambda x: x.lifetime > 0, self.shield_bonus_textes))
        for s in self.shield_bonus_textes: s.update(1, 1)


    def draw(self):

        self.screen.blit(self.background.image, self.background.rect)
        self.screen.blit(self.background.image, (self.background.rect.x, self.background.rect.y - self.background.rect.h))
        self.sprites.draw(self.screen)

        for score in self.score_textes:
            self.draw_text(score.text, 20, score.x, score.y, Color.WHITE.value)

        for bonus_text in self.shield_bonus_textes:
            self.draw_text(bonus_text.text, 20, bonus_text.x, bonus_text.y, Color.YELLOW.value)

        if self.player.shoot_bonus_counter > 0:
            self.draw_text(str(self.player.shoot_bonus_counter), \
                min(15 + 3*self.player.shoot_bonus_counter, config.WIDTH), \
                config.WIDTH//2, 50, Color.GREEN.value)

        self.draw_text(str(self.score), 20, config.WIDTH//2, 10, Color.WHITE.value)
        self.draw_shield_bar()
        self.draw_lives()


    def render(self):
        pygame.display.flip()


    def run(self):
        previous_tick = pygame.time.get_ticks()
        exec_time = 0
        wait_time = 0
        while self.running:
            while self.gameover:
                self.show_gameover_screen()
                self.init()
                self.gameover = False

            # execution time
            exec_time = pygame.time.get_ticks() - previous_tick
            # log.info("[exec_time] " + str(exec_time) + " ms")

            # wait until 1/FPS has passed (16.6666667 ms)
            self.clock.tick(config.FPS) # keep loop running at the right speed

            # measure time waited
            wait_time = pygame.time.get_ticks() - previous_tick - exec_time
            # log.info("[wait_time]" + str(wait_time) + " ms")
            # log.info("[wait_time + exec_time] " + str(wait_time + exec_time) + " ms") # should be 15 or 16

            print_percent_bar(exec_time, 16, True, '[0]', '[16]ms [exec_time='+str(exec_time)+'|wait_time='+str(wait_time)+']')

            # sample time right after the end of the waiting
            previous_tick = pygame.time.get_ticks()
            # log.info("[Start] " + str(previous_tick / 1000) + " s")

            self.process_inputs()
            self.update()
            self.draw()
            self.render()


        log.info("Exiting the Game.run() loop")
        pygame.quit()


# print percent bar. fraction must be float between 0 and 1
def print_percent_bar(squares, size=50, newLine=True, debuttext='', endtext=''):
    if squares > size: squares = size
    if squares < 0: squares = 0
    bar     = "▒" * ( int(squares) + 1) # "▓"
    nobar   = "░" * ( size - 1 - int(squares))
    if squares == size:
        bar = "█" * size
    print(debuttext, bar, nobar, endtext, sep='', end= '\n' if newLine else '')
