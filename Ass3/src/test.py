import math
import json
from pygame import *

from setting import *
from os import path

class Player(sprite.Sprite) :
    def __init__(self, game, x, y):

        self.groups = game.all_sprites
        sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = self.game.player_image
        self.rect = self.image.get_rect()
        self.velx = 0
        self.vely = 0
        self.width = self.rect.width
        self.height = self.rect.height

        # position of player
        self.rect.bottomleft = (x, y)

        # state of player
        self.stand = False
        self.runleft = False
        self.runright = False
        self.jump = False
        self.on_ground = False

    def update(self):
        if self.runleft:
            self.velx = -PLAYER_SPEED
        if self.runright:
            self.velx = PLAYER_SPEED
        if self.jump:
            if self.on_ground:
                self.vely = -JUMP_HEIGHT

        if not self.on_ground:
            self.vely += GRAVITY
            if self.vely > 8:
                self.vely = 8

        if not (self.runleft or self.runright):
            self.velx = 0
        self.rect.left += self.velx
        self.collide_with_walls(self.velx, 0)
        self.rect.bottom += self.vely
        self.on_ground = False
        self.collide_with_walls(0, self.vely)



    def collide_with_walls(self, vx, vy):
        for p in self.game.ground:
            if sprite.collide_rect(self, p):
                if vx > 0:
                    self.rect.right = p.rect.left
                if vx < 0:
                    self.rect.left = p.rect.right
                if vy > 0:
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.vely = 0
                if vy < 0:
                    self.rect.top = p.rect.bottom


class Ground(sprite.Sprite):
    def __init__(self, game, block):
        self.groups = game.all_sprites, game.ground
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = Surface((block["width"], block["height"]))
        Surface.set_alpha(self.image, 0)
        self.rect = self.image.get_rect()
        self.x = block["x"]
        self.y = block["y"]
        self.rect.left = self.x
        self.rect.top = self.y

class Enemy(sprite.Sprite):
    def __init__(self, game, block):
        self.groups = game.all_sprites, game.enemy
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = image.load(path.join(game_path,PLAYER_IMAGE))
        self.rect = self.image.get_rect()
        self.x = block["x"]
        self.y = block["y"]
        self.rect.left = self.x
        self.rect.top = self.y
        self.runleft = True
        self.runright = False
        
    def update(self):
        if self.runleft:
            self.velx = -PLAYER_SPEED
        if self.runright:
            self.velx = PLAYER_SPEED
        self.rect.left+=self.velx;
		if self.rect.left<=self.x-MARGIN_ENEMY:
            self.runright= True
            self.runleft=False
        if self.rect.left>=self.x+MARGIN_ENEMY:
            self.runleft= True
            self.runright=False
class Map:
    def __init__(self, file_path, background):
        self.data = []
        self.background = image.load(background)
        self.rect = self.background.get_rect()
        with open(file_path) as file:
            self.data = json.load(file)
        self.tilewidth = self.data["width"]
        self.tileheight = self.data["height"]
        self.width = self.tilewidth * TILE_SIZE
        self.height = self.tileheight * TILE_SIZE


class Camera:
    def __init__(self, screenwidth, screenheight):
        self.camera = Rect(0, 0, screenwidth, screenheight)
        self.width = screenwidth
        self.height = screenheight

    def apply(self, rect):
        return rect.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + int(WIDTH / 2)
        y = -player.rect.y + int(HEIGHT / 2)

        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom

        self.camera.x = x
        self.camera.y = y
        self.camera.width = WIDTH
        self.camera.height = HEIGHT



