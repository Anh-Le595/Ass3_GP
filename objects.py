import math
import json
from pygame import *
from os import path
import pygame

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
        self.x=x
        self.y=y+self.height
        self.margin=50

        self.Super = False
        # position of player
        self.rect.bottomleft = (x, y)
        self.battu = 0
        # score
        self.score = 0
        self.game.font_score = pygame.font.SysFont('ActionIsShaded', 50)
        self.game.total_score = self.game.font_score.render("Score : %d" % self.score, True, (255, 0, 0))

        #life
        self.score_life = 3
        self.game.score_life = pygame.font.SysFont('ActionIsShaded', 50)
        self.game.total_life = self.game.score_life.render("Life : %d" % self.score_life, True, (255, 0, 0))


        # state of player
        self.stand = False
        self.runleft = False
        self.runright = False
        self.jump = False
        self.climb = False
        self.dead = False
        self.on_ground = False
        self.on_ladder = False
        self.check_first_loop = False
        self.fall = True
        self.up = False
        self.shoot = False
        self.check_up = False
        self.check_down = False


        self.time = 10
        self.s = 0
        self.coord = 0
        self.count = 0

    def checkdirection(self):
        if self.runright:
            pos = self.rect.x + 32
            frame = (pos // 30) % len(list_run_frame_r)
            self.image = list_run_frame_r[frame]
        elif self.runleft:
            # print "2"
            pos = self.rect.x
            frame = (pos // 30) % len(list_run_frame_l)
            self.image = list_run_frame_l[frame]
        elif self.fall:
            # print "3"
            if self.count < len(list_run_frame_down):
                self.image = list_run_frame_down[self.count]
                # print (i,self.count)
                self.count += 1
            else:
                self.count = 0
        elif self.up:
            # print "4"
            if self.count < len(list_run_frame_up):
                self.image = list_run_frame_up[self.count]
                print (i,self.count)
                self.count += 1
            else:
                self.count = 0
        # elif self.stand == True:
        elif self.on_ground:
            # print "5"
            if self.count < len(list_run_frame_idle):
                self.image = list_run_frame_idle[self.count]
                self.count += 1
            else:
                self.count = 0
        # elif self.dead == True:
        #     if self.count < len(list_run_frame_dead):
        #         self.image = list_run_frame_dead[self.count]
        #         self.count += 1
        #     else:
        #         self.count = 0



    def collide_with_coin(self):
        for p in self.game.coin:
            if sprite.collide_rect(self,p):
                self.score += 1
                self.game.font_score = pygame.font.SysFont('ActionIsShaded', 50)
                self.game.total_score = self.game.font_score.render("Score : %d"%self.score, True, (255,0,0))
                p.kill()
    def update(self):
        if self.runleft:
            self.velx = -PLAYER_SPEED
        if self.runright:
            self.velx = PLAYER_SPEED
        if self.up:
            
            # print self.vely,self.rect.top
            if self.coord > self.s:
                self.coord -= JUMP_HEIGHT/len(list_run_frame_up)
                # print self.coord,self
                self.rect.top = self.coord
                self.up = True
            elif self.rect.top == self.s:
                # self.fall = True
                self.up = False
        if self.shoot:
            self.shoot_something()
            self.shoot = False
        # if self.rect.left<=self.x-self.margin:
        #     self.runright= True
        #     self.runleft=False
        #     self.shoot_something()
        # if self.rect.left>=self.x+self.margin:
        #     self.runleft= True
        #     self.runright=False
        #     self.shoot_something()

        if self.climb:
            if self.on_ground:
                self.rect.y -= 5
        if not self.on_ground:
            self.vely += GRAVITY
            if self.vely > 3:
                self.vely = 3
        if not (self.runleft or self.runright):
            self.velx = 0
        if self.jump:
            if self.on_ground:
                # self.vely = -JUMP_HEIGHT
                self.s = self.rect.top - JUMP_HEIGHT
                self.coord = self.rect.top
            self.up = True
        if self.vely == -JUMP_HEIGHT:
            self.fall = True
            
        # print (self.rect.top,self.vely)

        self.time -= 1
        if self.time == 0:
            self.checkdirection()
        if self.time < 0:
            self.time = 10
        self.collide_with_ladder()
        self.rect.left += self.velx
        self.collide_with_ground(self.velx, 0)
        self.collide_with_question(self.velx, 0)
        self.rect.bottom += self.vely
        self.collide_with_question(0, self.vely)
        self.collide_with_coin()
        self.on_ground = False
        self.collide_with_ground(0, self.vely)
        
        # print self.time
        # self.checkdirection()
        # self.count += 1
        # print self.count

    def shoot_something(self):
        vx=self.game.player.rect.centerx-self.rect.centerx
        disx = (self.game.player.rect.centerx-self.rect.centerx)
        disy = (self.game.player.rect.centery-self.rect.centery)
        self.energy+=1
        vx=BULLET_SPEED*disx/((disx*disx+disy*disy)**0.5)
        vy=BULLET_SPEED*disy/((disx*disx+disy*disy)**0.5)
        # if vx<0: 
            # vx=-BULLET_SPEED
        # else:
            # vx=BULLET_SPEED
        # vy = 0
        BulletPlayer(self.game,vx,vy,self)

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
                    self.fall = False
                if vy < 0:
                    self.rect.top = p.rect.bottom

    def collide_with_question(self, vx, vy):
        for p in self.game.life:
            if sprite.collide_rect(self, p):    
                if not p.destroy:
                    if vx > 0:
                        self.rect.right = p.rect.left

                    if vx < 0:
                        self.rect.left = p.rect.right
                    if vy > 0:
                        # print(self.on_ground)
                        self.rect.bottom = p.rect.top
                        self.on_ground = True
                        self.vely = 0
                        self.fall = False
                    if vy < 0:
                        self.rect.top = p.rect.bottom
                else:
                    self.score_life += 1
                    self.game.score_life = pygame.font.SysFont('ActionIsShaded', 50)
                    self.game.total_life = self.game.score_life.render("Score : %d"%self.score_life, True, (255,0,0))
                    # p.kill()
                    p.kill()
    def collide_with_ladder(self):
        for p in self.game.ladder:
            if sprite.collide_rect(self, p):
                if self.check_up == False:
                    self.rect.top = (p.rect.top + p.rect.bottom)/2 + 32
                # self.rect.top = (p.rect.top + p.rect.bottom)/2 + 32   
                # if self.rect.top == (p.rect.top + p.rect.bottom)/2 + 32:
                if key.get_pressed()[K_UP]:
                    # self.rect.left = p.rect.left
                    # self.vely = 0
                    # self.on_ground = True
                    # self.rect.bottom =  p.rect.top
                    self.check_up = True
                if self.check_up ==  True:
                    self.rect.bottom =  p.rect.top

                    if key.get_pressed()[K_DOWN]:
                #     # self.rect.left = p.rect.left
                #     # self.vely = 0
                #     # self.on_ground = True
                #     # self.rect.bottom =  p.rect.top
                        self.check_first_loop = False
                        self.check_down = True
                    if self.check_down ==  True and self.check_first_loop == False:
                        self.rect.top =  p.rect.bottom  
                        self.check_up = False
                        self.check_first_loop = True  
                self.on_ground = True
                    # if self.rect.bottom == p.rect.top:
                        # print "a"
                        # if key.get_pressed()[K_DOWN]:
                            # print "b"
                            # self.rect.x -= 10
                # if self.rect.bottom == p.rect.top:
                #     # self.rect.bottom = p.rect.top
                # # if self.check
                #     if key.get_pressed()[K_DOWN]:
                #         self.rect.top = p.rect.bottom  
                # if key.get_pressed()[K_DOWN]:
                # #     # self.rect.left = p.rect.left
                # #     # self.vely = 0
                # #     # self.on_ground = True
                # #     # self.rect.bottom =  p.rect.top
                #     self.check_down = True
                # if self.check_down ==  True:
                #     self.rect.top =  p.rect.bottom

                # self.check_up = False

    def shoot_something(self):
        BulletPlayer(self.game,BULLET_SPEED,0,self)
# class Bullet(sprite.Sprite):
#     def __init__(self, game, bullet):
#         self.groups = game.all_sprites, game.bullet
#         sprite.Sprite.__init__(self, self.groups)

#         self.game = game
#         # not have image
#         # self.image = image.load(path.join(game_path,))


class Coin(sprite.Sprite):
    def __init__(self, game, coin):
        self.groups = game.all_sprites, game.coin
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = image.load(COIN_IMG)
        self.image = transform.scale(self.image, (32, 32))

        self.rect = self.image.get_rect()
        self.x = coin["x"]
        self.y = coin["y"]
        self.rect.left = self.x
        self.rect.bottom = self.y

class Life(sprite.Sprite):
    def __init__(self, game, life):
        self.groups = game.all_sprites, game.life
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = image.load(BLOCK_IMG)
        self.image = transform.scale(self.image, (64, 64))

        self.rect = self.image.get_rect()
        self.x = life["x"]
        self.y = life["y"]
        self.rect.left = self.x
        self.rect.top = self.y
        self.destroy = False
        self.heart = False

class Ground(sprite.Sprite):
    def __init__(self, game, block):
        self.groups = game.all_sprites, game.ground
        sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.kind = block["type"]
        self.image = Surface((block["width"], block["height"]))
        self.image= image.load(path.join(game_path,"img/BrickBlockCastle.png"))
        self.image= transform.scale(self.image,(int(block["width"]),int(block["height"])))

        self.rect = self.image.get_rect()
        self.x = block["x"]
        self.y = block["y"]
        self.rect.left = self.x
        self.rect.top = self.y
    def load_img(self):
        pass

class BulletBoss(sprite.Sprite):
    def __init__(self, game,vx,vy,boss):
        self.groups = game.all_sprites, game.bulletboss
        sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vx=vx
        self.vy=vy
        self.image = image.load(path.join(game_path, "img/Objects/Bullet_000.png"))
        self.image = transform.scale(self.image, BULLET_SIZE)
        self.rect=self.image.get_rect()
        self.rect.center=boss.rect.center
        
        self.boss=boss
        self.count=0
    def update(self):
        self.rect.x+=self.vx
        # print (self.vx)
        if self.vx<0:
            self.vx+=3
            if self.vx>=-3:
                self.vx=-3
        if self.vx>0:
            self.vx-=3
            if self.vx<=3:
                self.vx=3
        self.rect.y+=self.vy;
        if self.count < len(bullet_run_frame):
            self.image = bullet_run_frame[self.count]
            if self.vx<0:
                self.image = transform.flip(self.image, True,False)
            self.count += 1
        else:
            self.count = 0
        if (((self.rect.centerx-self.boss.rect.centerx)**2+(self.rect.centery-self.boss.rect.centery)**2)**0.5)>500:
            self.kill()

class BulletPlayer(sprite.Sprite):
    def __init__(self, game,vx,vy,boss):
        self.groups = game.all_sprites, game.bulletplayer
        sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.vx=vx
        self.vy=vy
        self.image = image.load(path.join(game_path, "img/Objects/Bullet_000.png"))
        self.image = transform.scale(self.image, BULLET_SIZE)
        self.rect=self.image.get_rect()
        self.rect.center=boss.rect.center
        
        self.boss=boss
        self.count=0
    def update(self):
        self.rect.x+=self.vx
        # print (self.vx)
        if self.vx<0:
            self.vx+=3
            if self.vx>=-3:
                self.vx=-3
        if self.vx>0:
            self.vx-=3
            if self.vx<=3:
                self.vx=3
        self.rect.y+=self.vy;
        if self.count < len(bullet_run_frame):
            self.image = bullet_run_frame[self.count]
            if self.vx<0:
                self.image = transform.flip(self.image, True,False)
            self.count += 1
        else:
            self.count = 0
        if (((self.rect.centerx-self.boss.rect.centerx)**2+(self.rect.centery-self.boss.rect.centery)**2)**0.5)>500:
            self.kill()
        self.collide_with_questionblock()

    def collide_with_questionblock(self):
        for p in self.game.life:
            if sprite.collide_rect(self, p):
                self.kill()
                p.image = image.load(LIFE_IMG)
                p.destroy = True

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



class GameMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load(TITLE_SCREEN)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.instruction_image = pygame.image.load(INSTRUCTION_SCREEN)
        self.instruction_image = pygame.transform.scale(self.instruction_image, (WIDTH, HEIGHT))
        self.instruct_image = pygame.image.load(KHUNG_PATH)
        self.btnStart = Button(0)
        self.btnInstruct = Button(1)
        self.btnQuit = Button(3)
        self.btnBack = Button(2)
        self.titleLoop = True
        self.instructionLoop = False
        self.mainLoop = True

    def draw_title(self):
        while self.mainLoop:
            while self.titleLoop:
                self.clock.tick(FPS)
                self.screen.blit(self.image, (0, 0))
                self.mouse = pygame.mouse.get_pos()
                self.btnStart.draw(self.screen, self.mouse, (340, 250),(100,60))
                self.btnInstruct.draw(self.screen, self.mouse, (315, 335),(160,60))
                self.btnQuit.draw(self.screen, self.mouse, (340, 420),(100,50))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.titleLoop = False
                        pygame.quit()
                        exit()
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

            while self.instructionLoop:
                self.screen.blit(self.instruction_image, (0, 0))
                self.screen.blit(self.instruct_image, (180, 0))
                self.mouse = pygame.mouse.get_pos()
                self.btnBack.draw(self.screen, self.mouse, (340, 350),(100,50))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.instructionLoop = False
                        self.mainLoop = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.btnBack.obj.collidepoint(self.mouse):
                            self.instructionLoop = False
                            self.titleLoop = True

                self.clock.tick(FPS)

class GameGO:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.image = pygame.image.load(GO_SCREEN)
        self.image = pygame.transform.scale(self.image, (WIDTH, HEIGHT))
        self.mainLoop = True
        self.btnAgain = Button(5)
        self.btnMainMenu = Button(4)
    def draw_gameover(self):
        # pygame.init()
        while self.mainLoop:
            self.clock.tick(FPS)
            self.screen.blit(self.image, (0, 0))
            self.mouse = pygame.mouse.get_pos()
            self.btnAgain.draw(self.screen, self.mouse, (300, 220),(180,70))
            self.btnMainMenu.draw(self.screen, self.mouse, (300, 320),(180,70))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.btnAgain.obj.collidepoint(self.mouse):
                        self.mainLoop = False
                        return True
                    elif self.btnMainMenu.obj.collidepoint(self.mouse):
                        self.mainLoop = False
                        return False

class Button:
    def __init__(self,index):
        self.indexbutton = index
        self.is_hover = False
        self.default_color = (100,100,100)
        self.hover_color = (255,255,255)
        self.image = None
        self.obj = None


    def color(self):
        '''change color when hovering'''
        if self.is_hover:
            return self.hover_color
        else:
            return self.default_color

    def button_load(self):
        if self.indexbutton == 0:
            self.image = pygame.image.load(START_BUTTON)
        elif self.indexbutton == 1:
            self.image = pygame.image.load(INSTRUCT_BUTTON)
        elif self.indexbutton == 2:
            self.image = pygame.image.load(BACK_BUTTON)
        elif self.indexbutton == 3:
            self.image = pygame.image.load(QUIT_BUTTON)
        elif self.indexbutton == 4:
            self.image = pygame.image.load(MMENU_BUTTON)
        elif self.indexbutton == 5:
            self.image = pygame.image.load(PAGAIN_BUTTON)


    def draw(self, screen, mouse, rectcoord, size):
        '''create rect obj, draw, and change color based on input'''
        self.button_load()
        self.image = pygame.transform.scale(self.image,size)
        self.obj = screen.blit(self.image, rectcoord)

        # change color if mouse over button
        self.check_hover(mouse)

    def check_hover(self, mouse):
        '''adjust is_hover value based on mouse over button - to change hover color'''
        if self.obj.collidepoint(mouse):
            self.is_hover = True
        else:
            self.is_hover = False
