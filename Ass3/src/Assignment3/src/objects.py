import math
import json
from pygame import *
from os import path

from setting import *


class Player(sprite.Sprite):
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

        self.Super = False
        # position of player
        self.rect.bottomleft = (x, y)
        self.battu = 0
        # score
        self.score = 0
        self.game.font_score = pygame.font.SysFont('ActionIsShaded', 50)
        self.game.total_score = self.game.font_score.render("Score : %d" % self.score, True, (255, 0, 0))

        # state of player
        self.stand = False
        self.runleft = False
        self.runright = False
        self.jump = False
        self.climb = False
        self.dead = False
        self.on_ground = False
        self.on_ladder = False

        self.count = 0

    def checkdirection(self):
        if self.runright == True:
            pos = self.rect.x + 32
            frame = (pos // 30) % len(list_run_frame_r)
            # print "frame" + str(frame) + "len" + str(len(list_run_frame_r))
            self.image = list_run_frame_r[frame]
        elif self.runleft == True:
            pos = self.rect.x
            frame = (pos // 30) % len(list_run_frame_l)
            # print "frame" + str(frame) + "len" + str(len(list_run_frame_l))
            self.image = list_run_frame_l[frame]
        # elif (self.jump == True and self.runright) or (self.jump == True and self.runleft == True):
        elif self.jump == True:
            # pos = self.rect.y
            # frame = (pos // 30) % len(list_run_frame_up)
            if self.count < len(list_run_frame_up):
                self.image = list_run_frame_up[self.count]
                # print (i,self.count)
                self.count += 1
            else:
                self.count = 0
        elif self.stand == True:
            if self.count < len(list_run_frame_idle):
                self.image = list_run_frame_idle[self.count]
                self.count += 1
            else:
                self.count = 0
        elif self.dead == True:
            if self.count < len(list_run_frame_dead):
                self.image = list_run_frame_idle[self.count]
                self.count += 1
            else:
                self.count = 0


    def update(self):
        if self.runleft:
            self.velx = -PLAYER_SPEED
        if self.runright:
            self.velx = PLAYER_SPEED
        if self.jump:
            if self.on_ground:
                self.vely = -JUMP_HEIGHT
        if self.climb:
            if self.on_ground:
                self.rect.y -= 5
        if not self.on_ground:
            self.vely += GRAVITY
            if self.vely > 3:
                self.vely = 3
        if not (self.runleft or self.runright):
            self.velx = 0
        self.collide_with_ladder()
        self.rect.left += self.velx
        self.collide_with_ground(self.velx, 0)
        self.rect.bottom += self.vely
        self.on_ground = False
        self.collide_with_ground(0, self.vely)
        self.checkdirection()


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

    def collide_with_ladder(self):
        for p in self.game.ladder:
            if sprite.collide_rect(self, p):
                if self.jump == True:
                    if self.rect.top == (p.rect.top + p.rect.bottom)/2:
                        if key.get_pressed()[K_UP]:
                            self.rect.left = p.rect.left
                            self.vely = 0
                            self.on_ground = True
                            self.rect.y -= 1
                if key.get_pressed()[K_DOWN]:
                    if self.rect.bottom == p.rect.top:
                        self.rect.x -= 10


class Bullet(sprite.Sprite):
    def __init__(self, game, bullet):
        self.groups = game.all_sprites, game.bullet
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        # not have image
        # self.image = image.load(path.join(game_path,))





class Ground(sprite.Sprite):
    def __init__(self, game, block):
        self.groups = game.all_sprites, game.ground
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.kind = block["type"]
        self.image = Surface((block["width"], block["height"]))
        self.image.fill(WHITE)

        self.rect = self.image.get_rect()
        self.x = block["x"]
        self.y = block["y"]
        self.rect.left = self.x
        self.rect.top = self.y
    def load_img(self):
        pass


class Ladder(sprite.Sprite):
    def __init__(self, game, ladder):
        self.groups = game.all_sprites, game.ladder
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = Surface((ladder["width"], ladder["height"]))
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.x = ladder["x"]
        self.y = ladder["y"]
        self.rect.left = self.x
        self.rect.top = self.y
    def load_img(self):
        pass




class Map:
    def __init__(self, file_path):
        self.data = []
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


