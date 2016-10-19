from os import path
import pygame
from pygame import *


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (100, 100, 100)
GREY = (40, 40, 40)



# game setting

TILE_SIZE = 128
BLOCK_SIZE = (TILE_SIZE, TILE_SIZE)


FPS = 60
WIDTH = 6 * TILE_SIZE
HEIGHT = 5 * TILE_SIZE
CAPTION = "Mario Azawa"
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

GRAVITY = 3



# player setting
PLAYER_SPEED = 3
JUMP_HEIGHT = 20
PLAYER_IMAGE = "images/MarioStanding.png"
PLAYER_UP_IMAGE = "images/SuperMarioStanding.png"
RUN = "img/Run (1).png"
# enemy
MARGIN_ENEMY=20
ENEMY_SPEED =1
ENEMY_IMAGE = "images/enemy.gif"

# paths
game_path = path.dirname(__file__)
# MAP1_PATH = "map_2/map1_1.json"
# BACKGROUND1_PATH = "map_2/background1_1.png"
# MAP2_PATH = "map_2/map_boss.json"
# BACKGROUND2_PATH = "map2/background_boss.png"
MAP_PATH = "map/map.json"

# in_x = 2394
# in_y = 331
#
# out_x = 2618
# out_y = 144

# image
TITLE_SCREEN = 'images/TitleScreen.png'
GO_SCREEN = "images/GOScreen.png"
INSTRUCTION_SCREEN = "images/Instruction.png"

# Sprite run
list_run_frame_r = []
list_run_frame_l = []
list_run_frame_up = []
list_run_frame_idle = []
list_run_frame_dead = []
# runleft
for i in range(8):
    images = image.load(path.join(game_path,"img/Run (" + str(i+1)+").png"))
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_r.append(images)
# runright
for i in range(8):
    images = image.load(path.join(game_path,"img/Run (" + str(i+1)+").png"))
    images = transform.flip(images, True, False)
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_l.append(images)
# jump
for i in range(10):
    images = image.load(path.join(game_path,"img/Jump (" + str(i+1)+").png"))
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_up.append(images)
# idle
for i in range(10):
    images = image.load(path.join(game_path,"img/Idle (" + str(i+1)+").png"))
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_idle.append(images)
# dead
for i in range(10):
    images = image.load(path.join(game_path,"img/Dead (" + str(i+1)+").png"))
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_dead.append(images)
