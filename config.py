

"""
"""


import os


# Game config

WIDTH   = 480
HEIGHT  = 594
FPS     = 60
DIFFICULTY = 1.5 # multiplier of speed
NB_MOBS = 24

power_up_types = ['shield', 'bolt']
power_up_levels = ['bronze', 'silver', 'gold']


# Folder of this config file (must be at the root of project)

game_folder = os.path.dirname(__file__)


# Images

img_folder  = os.path.join(game_folder, "img")
snd_folder  = os.path.join(game_folder, "snd")
font_folder = os.path.join(game_folder, "fnt")

meteors_folder = os.path.join(img_folder, "meteors")
explosion_folder = os.path.join(img_folder, "explosion")

background = os.path.join(img_folder, "starfield.png")

meteor_filenames = [
    os.path.join(meteors_folder, "meteorBrown_big1.png"),
    os.path.join(meteors_folder, "meteorBrown_big2.png"),
    os.path.join(meteors_folder, "meteorBrown_big3.png"),
    os.path.join(meteors_folder, "meteorBrown_big4.png"),

    os.path.join(meteors_folder, "meteorBrown_med1.png"),
    os.path.join(meteors_folder, "meteorBrown_med3.png"),

    os.path.join(meteors_folder, "meteorBrown_small1.png"),
    os.path.join(meteors_folder, "meteorBrown_small2.png"),

    os.path.join(meteors_folder, "meteorBrown_tiny1.png"),
    os.path.join(meteors_folder, "meteorBrown_tiny2.png"),
]

regular_explosion_filenames = [os.path.join(explosion_folder, 'regularExplosion0{}.png'.format(i)) for i in range(9)]
sonic_explosion_filenames = [os.path.join(explosion_folder, 'sonicExplosion0{}.png'.format(i)) for i in range(9)]

laser_images = dict( (color, os.path.join(img_folder, "laser_{}.png".format(color))) \
                      for color in ('red', 'green', 'blue_ball', 'blue_cross', 'red_ball') )

power_up_images = dict ( (type + "_" + level, os.path.join(img_folder, "{}_{}.png".format(type, level))) \
                         for type in power_up_types for level in power_up_levels)


player_ship = os.path.join(img_folder, "playerShip1_blue.png")
player_life = os.path.join(img_folder, "playerLife1_blue.png")


# Font

font_name = os.path.join(font_folder, "kenvector_future.ttf")


# Sounds

l1   = os.path.join(snd_folder, "Laser_Shoot1.wav")
l2   = os.path.join(snd_folder, "Laser_Shoot2.wav")
l3   = os.path.join(snd_folder, "Laser_Shoot3.wav")
l4   = os.path.join(snd_folder, "Laser_Shoot4.wav")
e1   = os.path.join(snd_folder, "Explosion1.wav")
e2   = os.path.join(snd_folder, "Explosion2.wav")
e3   = os.path.join(snd_folder, "Explosion3.wav")
ep   = os.path.join(snd_folder, "rumble1.ogg")
pc2  = os.path.join(snd_folder, "Pickup_Coin2.wav")
p6   = os.path.join(snd_folder, "Powerup6.wav")

background_music = os.path.join(snd_folder, "gresille.ogg")
