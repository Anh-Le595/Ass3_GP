from os import path
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
PLAYER_SPEED = 10
JUMP_HEIGHT = 24
PLAYER_IMAGE = "images/MarioStanding.png"


# paths
game_path = path.dirname(__file__)
MAP1_PATH = "map/map1_1.json"
BACKGROUND1_PATH = "map/background1_1.png"
