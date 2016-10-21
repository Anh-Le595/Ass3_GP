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
BLOCK_SIZE = (64, 64)


FPS = 60
WIDTH = 6 * TILE_SIZE
HEIGHT = 5 * TILE_SIZE
CAPTION = "Mario Azawa"
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

GRAVITY = 30



# player setting
PLAYER_SPEED = 8
JUMP_HEIGHT = 64
PLAYER_IMAGE = "images/MarioStanding.png"
PLAYER_UP_IMAGE = "images/SuperMarioStanding.png"
RUN = "img/Run (1).png"
# enemy
MARGIN_ENEMY=20
ENEMY_SPEED =1
ENEMY_IMAGE = "images/enemy.gif"

# Sprite run
BOSS_SPEED = 4
BOSS_SIZE =(128,128)
BULLET_SIZE=(32,32)
BULLET_SPEED=8
BOSS_JUMP_HEIGHT = 30
MARGIN_BOSS = 30

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


# item
COIN_IMG = path.join(game_path, "img/Objects/Coin.gif")
KEY_IMG = path.join(game_path, "img/Objects/Axe.gif")
LIFE_IMG = path.join(game_path, "img/Objects/Heart.gif")
BLOCK_IMG = path.join(game_path, "img/Objects/Block.gif")



# image
TITLE_SCREEN = 'images/TitleScreen.png'
GO_SCREEN = "images/GOScreen.png"
INSTRUCTION_SCREEN = "images/Instruction.png"

# Sprite run
list_run_frame_r = []
list_run_frame_l = []
list_run_frame_up = []
list_run_frame_down = []
list_run_frame_idle = []
list_run_frame_dead = []
bullet_run_frame =[]

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
for i in range(6):
    images = image.load(path.join(game_path,"img/Jump (" + str(i+1)+").png"))
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_up.append(images)
# fall
for i in range(6,10):
    images = image.load(path.join(game_path,"img/Jump (" + str(i+1)+").png"))
    images = transform.scale(images,BLOCK_SIZE)
    list_run_frame_down.append(images)
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
# bullet
for i in range(4):
    images = image.load(path.join(game_path,"img/Objects/Bullet_00"+str(i)+".png"))
    images = transform.scale(images,(32,32))
    bullet_run_frame.append(images)

START_BUTTON = "images/start.png"
INSTRUCT_BUTTON = "images/instruct.png"
BACK_BUTTON = "images/back.png"
QUIT_BUTTON = "images/quit.png"
PAGAIN_BUTTON = "images/playagain.png"
MMENU_BUTTON = "images/mainmenu.png"
KHUNG_PATH = "images/khung.png"
TITLE_SCREEN = 'images/TitleScreen.png'
GO_SCREEN = "images/GOScreen.png"
INSTRUCTION_SCREEN = "images/Instruction.png"
BOSS_SPEED = 4
BOSS_SIZE =(128,128)
BULLET_SIZE=(32,32)
BULLET_SPEED=8
BOSS_JUMP_HEIGHT = 30
MARGIN_BOSS = 30
boss_run_frame_r = []
boss_run_frame_l = []
boss_run_frame_up = []
boss_run_frame_idle = []
boss_run_frame_dead = []
bullet_run_frame =[]
# runleft
for i in range(8):
    images = image.load(path.join(game_path,"img/png/Run (" + str(i+1)+").png"))
    images = transform.scale(images,BOSS_SIZE)
    boss_run_frame_r.append(images)
# runright
for i in range(8):
    images = image.load(path.join(game_path,"img/png/Run (" + str(i+1)+").png"))
    images = transform.flip(images, True, False)
    images = transform.scale(images,BOSS_SIZE)
    boss_run_frame_l.append(images)
# jump
for i in range(8):
    images = image.load(path.join(game_path,"img/png/JumpAttack (" + str(i+1)+").png"))
    images = transform.scale(images,BOSS_SIZE)
    boss_run_frame_up.append(images)
# idle
for i in range(10):
    images = image.load(path.join(game_path,"img/png/Idle (" + str(i+1)+").png"))
    images = transform.scale(images,BOSS_SIZE)
    boss_run_frame_idle.append(images)
# dead
for i in range(10):
    images = image.load(path.join(game_path,"img/png/Dead (" + str(i+1)+").png"))
    images = transform.scale(images,BOSS_SIZE)
    boss_run_frame_dead.append(images)