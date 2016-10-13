from os import path
import pygame
from pygame.locals import *


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GREY = (100, 100, 100)



# game setting
FPS = 60
WIDTH = 800
HEIGHT = 480
CAPTION = "Mario Azawa"


GRAVITY = 3

TILE_SIZE = 32
BLOCK_SIZE = (TILE_SIZE, TILE_SIZE)
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

# player setting
PLAYER_SPEED = 3
JUMP_HEIGHT = 24
PLAYER_IMAGE = "images/MarioStanding.png"
PLAYER_UP_IMAGE = "images/SuperMarioStanding.png"

# enemy
MARGIN_ENEMY=20
ENEMY_SPEED =1
ENEMY_IMAGE = "images/enemy.gif"

# paths
game_path = path.dirname(__file__)
MAP1_PATH = "map_1/map1_1.json"
BACKGROUND1_PATH = "map_1/background1_1.png"


in_x = 2394
in_y = 331

out_x = 2618
out_y = 144

# image
TITLE_SCREEN = 'images/TitleScreen.png'
GO_SCREEN = "images/GOScreen.png"
INSTRUCTION_SCREEN = "images/Instruction.png"