import math
import json
from pygame import *
from os import path

from setting import *


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
        self.collide_with_ground(self.velx, 0)
        self.collide_with_brick(self.velx, 0)
        self.rect.bottom += self.vely
        self.on_ground = False
        self.collide_with_ground(0, self.vely)
        self.collide_with_brick(0,self.vely)




    def collide_with_ground(self, vx, vy):
        for p in self.game.ground:
            if sprite.collide_rect(self, p):
                if vx > 0:
                    self.rect.right = p.rect.left
                if vx < 0:
                    self.rect.left = p.rect.right
                if vy > 0:
                    # print(self.on_ground)
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.vely = 0
                if vy < 0:
                    self.rect.top = p.rect.bottom

    def collide_with_brick(self,vx,vy):
        for p in self.game.brick:
            if sprite.collide_rect(self, p):
                if vx > 0:
                    self.rect.right = p.rect.left
                if vx < 0:
                    self.rect.left = p.rect.right
                if vy > 0:
                    # print(self.on_ground)
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.vely = 0
                if vy < 0:
                    #dap be brick
                    p.kill()



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


class Brick(sprite.Sprite):
    def __init__(self,game,brick):
        self.groups = game.all_sprites, game.brick
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = image.load(path.join(game_path,"images/brick.png"))
        self.rect = self.image.get_rect()
        self.x = brick["x"]
        self.y = brick["y"]
        self.rect.left = self.x
        self.rect.top = self.y

class questionBlock(sprite.Sprite):
    def __init__(self,game,questionblock):
        self.groups = game.all_sprites, game.questionblock
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = image.load(path.join(game_path,"images/QuestionBlock.gif"))
        self.rect = self.image.get_rect()
        self.x = questionblock["x"]
        self.y = questionblock["y"]
        self.rect.left = self.x
        self.rect.top = self.y

class Coin(sprite.Sprite):
    def __init__(self,game,coin):
        self.groups = game.all_sprites, game.coin
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = image.load(path.join(game_path,"images/Coin.gif"))
        self.rect = self.image.get_rect()
        self.x = coin["x"]
        self.y = coin["y"]
        self.rect.left = self.x
        self.rect.top = self.y

class Mushroom(sprite.Sprite):
    def __init__(self,game,mushroom):
        self.groups = game.all_sprites, game.mushroom
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = image.load(path.join(game_path,"images/mushroom.png"))
        self.rect = self.image.get_rect()
        self.x = mushroom["x"]
        self.y = mushroom["y"]
        self.rect.left = self.x
        self.rect.top = self.y

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



