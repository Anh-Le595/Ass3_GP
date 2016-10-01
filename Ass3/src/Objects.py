import math
from pygame import *
from setting import *


class Player(sprite.Sprite) :
    def __init__(self, game, x, y):

        self.groups = game.all_sprites
        sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = self.game.player_image
        self.rect = self.image.get_rect()
        # self.vel = math.Vector2(0, 0)
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
        print(self.on_ground)
        print(vx,vy)
        for p in self.game.ground:
            if sprite.collide_rect(self, p):
                if vx > 0:
                    self.rect.right = p.rect.left
                if vx < 0:
                    self.rect.left = p.rect.right
                if vy > 0:
                    print(self.on_ground)
                    self.rect.bottom = p.rect.top
                    self.on_ground = True
                    self.vely = 0
                if vy < 0:
                    self.rect.top = p.rect.bottom

class Ground(sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.ground
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = self.x * TILE_SIZE
        self.rect.bottom = self.y * TILE_SIZE

class Map:
    def __init__(self, file_path):
        self.data = []
        with open(file_path,'r') as file:
            for line in file:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILE_SIZE
        self.height = self.tileheight * TILE_SIZE

class Camera:
    def __init__(self, screenwidth, screenheight):
        self.camera = Rect(0,0, screenwidth, screenheight)
        self.width = screenwidth
        self.height = screenheight

    def apply(self, object):
        return object.rect.move(self.camera.topleft)

    def update(self, player):
        x = -player.rect.x + int(WIDTH / 2)
        y = -player.rect.y + int(HEIGHT / 2)

        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom

        self.camera.x = x
        self.camera.y = y
        self.camera.width = self.width
        self.camera.height = self.height




