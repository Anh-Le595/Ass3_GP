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
        
        self.Super = False
        # position of player
        self.rect.bottomleft = (x, y)

        # score
        self.score = 0
        self.game.font_score = pygame.font.SysFont('ActionIsShaded', 50)
        self.game.total_score = self.game.font_score.render("Score : %d"%self.score, True, (255,0,0))

        
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
        self.collide_with_coin()
        self.collide_with_brick(self.velx, 0)
        self.collide_with_questionblock(self.velx, 0)
        self.rect.bottom += self.vely
        self.on_ground = False
        self.collide_with_ground(0, self.vely)
        self.collide_with_coin()
        self.collide_with_brick(0,self.vely)
        self.collide_with_questionblock(0,self.vely)
        self.collide_with_deadzone()
        self.collide_with_mushroom()
        self.collide_with_enemy(self.velx, self.vely)


    def collide_with_ground(self, vx, vy):
        for p in self.game.ground:
            if sprite.collide_rect(self, p):
                if vx > 0:
                    
                    if p.kind == "out":
                        if key.get_pressed()[K_RIGHT]:
                            self.rect.x = out_x
                            self.rect.y = out_y
                        else:
                            self.rect.right = p.rect.left
                    else:
                        self.rect.right = p.rect.left


                if vx < 0:
                    self.rect.left = p.rect.right
                if vy > 0:
                    # print(self.on_ground)
                    if p.kind == "in":
                        if key.get_pressed()[K_DOWN]:
                            self.rect.x = in_x
                            self.rect.y = in_y
                        else:
                            self.rect.bottom = p.rect.top
                            self.on_ground = True
                            self.vely = 0
                    else :
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
                    if self.Super:
                        p.kill()
                    else:
                        self.rect.top = p.rect.bottom

    def collide_with_coin(self):
        for p in self.game.coin:
            if sprite.collide_rect(self,p):
                self.score += 1
                self.game.font_score = pygame.font.SysFont('ActionIsShaded', 50)
                self.game.total_score = self.game.font_score.render("Score : %d"%self.score, True, (255,0,0))
                p.kill()

    def collide_with_mushroom(self):
        for p in self.game.mushroom:
            if sprite.collide_rect(self,p):
                self.image = image.load(path.join(game_path,PLAYER_UP_IMAGE))
                self.Super = True
                self.rect.height = self.image.get_rect().height
                self.rect.width = self.image.get_rect().width 
                # self.rect = self.image.get_rect()
                # self.bottomleft = self.rect.x + self.velx
                self.rect.bottomleft = (self.rect.left,self.rect.bottom-16)
                p.kill()
    def collide_with_deadzone(self):
        for p in self.game.deadzone:
            if sprite.collide_rect(self,p):
                self.rect.bottom = p.rect.top
                self.on_ground = True
                self.vely = 0
                self.game.gameover = True
            # return True
    def collide_with_questionblock(self,vx,vy):
        for p in self.game.questionblock:
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
                    if not p.empty:
                        if p.item == "nam":
                            p.image = image.load(path.join(game_path,"images/EmptyBlock.png"))
                            Mushroom(self.game, p.rect.x, p.rect.y -16)
                            p.empty = True
                        else :
                            p.image = image.load(path.join(game_path,"images/EmptyBlock.png"))
                            a = Coin(self.game,p.rect.x,p.rect.y-16)
                            p.empty = True
                            a.disable = True
                            self.score += 1
                            self.game.font_score = pygame.font.SysFont('ActionIsShaded', 50)
                            self.game.total_score = self.game.font_score.render("Score : %d"%self.score, True, (255,0,0))
                    self.rect.top = p.rect.bottom


    def collide_with_enemy(self, vx, vy):
        for p in self.game.enemy:
            if sprite.collide_rect(self, p):
                if vy==0:
                    if self.rect.centerx<p.rect.left:
                        self.rect.right = p.rect.left
                    if self.rect.centerx>p.rect.right:
                        self.rect.left = p.rect.right
                    self.game.playing=False
                if vy > 0:
                    self.rect.bottom = p.rect.bottom
                    self.on_ground = True
                    self.vely = 0
                    p.kill()
                if self.rect.bottom  == p.rect.top and p.rect.left + p.rect.width/2 - 16 == self.rect.left + self.rect.width/2:
                    p.kill()

class Ground(sprite.Sprite):
    def __init__(self, game, block):
        self.groups = game.all_sprites, game.ground
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.kind = block["type"]
        self.image = Surface((block["width"], block["height"]))
        Surface.set_alpha(self.image, 0)
        self.rect = self.image.get_rect()
        self.x = block["x"]
        self.y = block["y"]
        self.rect.left = self.x
        self.rect.top = self.y

class Deadzone(sprite.Sprite):
    def __init__(self, game, deadzone):
        self.groups = game.all_sprites, game.deadzone
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = Surface((deadzone["width"], deadzone["height"]))
        Surface.set_alpha(self.image, 0)
        self.rect = self.image.get_rect()
        self.x = deadzone["x"]
        self.y = deadzone["y"]
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

        self.item = questionblock["type"]
        self.image = image.load(path.join(game_path,"images/QuestionBlock.gif"))
        self.rect = self.image.get_rect()
        self.x = questionblock["x"]
        self.y = questionblock["y"]
        self.rect.left = self.x
        self.rect.top = self.y
        self.empty = False

class Coin(sprite.Sprite):
    def __init__(self,game,x,y):
        self.groups = game.all_sprites, game.coin
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.disable= False
        self.image = image.load(path.join(game_path,"images/Coin.gif"))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = self.x
        self.rect.top = self.y
    def update(self):
        if self.disable:
            self.kill()

class Mushroom(sprite.Sprite):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites, game.mushroom
        sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.image = image.load(path.join(game_path,"images/mushroom.png"))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left = self.x
        self.rect.top = self.y

# class Enemy(sprite.Sprite):
#     def __init__(self,game, enemy):
#         self.groups = game.all_sprites, game.enemy
#         sprite.Sprite.__init__(self, self.groups)

#         self.game = game

#         self.image = image.load(path.join(game_path,"images/enemy.gif"))
#         self.rect = self.image.get_rect()
#         self.x = enemy["x"]
#         self.y = enemy["y"]
#         self.rect.left = self.x
#         self.rect.top = self.y
class Enemy(sprite.Sprite):
    def __init__(self, game, block):
        self.groups = game.all_sprites, game.enemy
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.visible = block["visible"]
        self.alive= block["visible"]
        self.image = image.load(path.join(game_path,ENEMY_IMAGE))
        self.rect = self.image.get_rect()
        self.x = block["x"]
        self.y = block["y"]
        self.rect.left = self.x
        self.rect.top = self.y
        self.runleft = True
        self.runright = False

    def update(self):
        if self.runleft:
            self.velx = -ENEMY_SPEED
        if self.runright:
            self.velx = ENEMY_SPEED
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





class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load(TITLE_SCREEN)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.instruction_image = pygame.image.load(INSTRUCTION_SCREEN)
        self.instruction_image = pygame.transform.scale(self.instruction_image, (WIDTH, HEIGHT))
        self.btnStart = Button('START')
        self.btnInstruct = Button('INSTRUCTION')
        self.btnQuit = Button('QUIT')
        self.btnBack = Button('BACK')
        self.titleLoop = True
        self.instructionLoop = False
        self.mainLoop = True

    def draw_title(self):
        while self.mainLoop:
            while self.titleLoop:
                self.clock.tick(FPS)
                self.screen.blit(self.image, (0, 0))
                self.mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.titleLoop = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.btnQuit.obj.collidepoint(self.mouse):
                            self.titleLoop = False
                            self.instructionLoop = False
                            self.mainLoop = False
                            pygame.quit()
                        elif self.btnStart.obj.collidepoint(self.mouse):
                            self.titleLoop = False
                            self.instructionLoop = False
                            self.mainLoop = False
                        elif self.btnInstruct.obj.collidepoint(self.mouse):
                            self.titleLoop = False
                            self.instructionLoop = True
                self.btnStart.draw(self.screen, self.mouse, (340, 270, 130, 40), (375, 278))
                self.btnInstruct.draw(self.screen, self.mouse, (340, 350, 130, 40), (357, 358))
                self.btnQuit.draw(self.screen, self.mouse, (340, 430, 130, 40), (380, 438))
                pygame.display.flip()
            while self.instructionLoop:
                self.screen.blit(self.instruction_image, (0, 0))
                self.mouse = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.instructionLoop = False
                        self.mainLoop = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.btnBack.obj.collidepoint(self.mouse):
                            self.instructionLoop = False
                            self.titleLoop = True
                self.btnBack.draw(self.screen, self.mouse, (340, 350, 120, 40), (373, 355))
                pygame.display.flip()
                self.clock.tick(FPS)

class GameGO:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load(GO_SCREEN)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.mainLoop = True

    def draw_gameover(self):
        # pygame.init()
        while self.mainLoop:
            self.clock.tick(FPS)
            self.screen.blit(self.image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            pygame.display.flip()
class Button:
    def __init__(self,text):
        self.text = text
        self.is_hover = False
        self.default_color = (100,100,100)
        self.hover_color = (255,255,255)
        self.font_color = (0,0,0)
        self.obj = None

    def label(self):
        font = pygame.font.Font("FreeSansBold.ttf", 14)
        return font.render(self.text, 1, self.font_color)

    def color(self):
        '''change color when hovering'''
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color

    def draw(self, screen, mouse, rectcoord, labelcoord):
        '''create rect obj, draw, and change color based on input'''
        self.obj = pygame.draw.rect(screen, self.color(), rectcoord)
        screen.blit(self.label(), labelcoord)

        # change color if mouse over button
        self.check_hover(mouse)

    def check_hover(self, mouse):
        '''adjust is_hover value based on mouse over button - to change hover color'''
        if self.obj.collidepoint(mouse):
            self.is_hover = True
        else:
            self.is_hover = False
