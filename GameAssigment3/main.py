from os import path
import pygame
from pygame import *
from Objects import *
from setting import *


class Main:
    def __init__(self):
        # init GameWindow, etc
        init()
        self.screen = display.set_mode((WIDTH, HEIGHT))
        display.set_caption(CAPTION)
        self.clock = time.Clock()
        # self.player_image = image.load(path.join(game_path, PLAYER_IMAGE))
        # self.player_image = self.list_run_frame_r[0]
        self.player_image = image.load(path.join(game_path,RUN))
        self.player_image = transform.scale(self.player_image,(32,32))
        self.map = Map(path.join(game_path, MAP1_PATH), path.join(game_path, BACKGROUND1_PATH))
        self.running = True
        self.gameover = False
        
    def new(self):
        # start a new game

        # create all sprites
        self.all_sprites = sprite.Group()
        self.deadzone = sprite.Group()
        self.ground = sprite.Group()
        self.brick = sprite.Group()
        self.questionblock = sprite.Group()
        self.mushroom = sprite.Group()
        self.coin = sprite.Group()
        self.enemy = sprite.Group()

        for layer in self.map.data["layers"]:
            if layer["name"] == "Ground":
                for ground in layer["objects"]:
                    Ground(self, ground)
            if layer["name"] == "GameZone":
                for zone in layer["objects"]:
                    if zone["name"] == "deadzone":
                        Deadzone(self,zone)
            if layer["name"] == "Player":
                self.player = Player(self, layer["objects"][0]["width"], layer["objects"][0]["height"])
            if layer["name"] == "Brick":
                for brick in layer["objects"]:
                    Brick(self, brick)
            if layer["name"] == "QuestionBlock":
                for questionblock in layer["objects"]:
                    questionBlock(self, questionblock)
            if layer["name"] == "Enemy":
                for enemy in layer["objects"]:
                    Enemy(self,enemy)
                
                # coin will display on screen, not in questionblock 
            if layer["name"] == "Item":
                for item in layer["objects"]:
                    if item["name"] == "coin":
                        Coin(self,item["x"],item["y"])
                    
            

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing :
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            if self.gameover:
                # print "run"
                # self.running = False
                # self.screen.fill(WHITE)
                # self.text_over = font.SysFont('ActionIsShaded', 50)
                # self.screen_overgame = self.text_over.render("Game Over",True, (255,0,0))
                # self.screen.blit(self.screen_overgame,(WIDTH/2,HEIGHT/2))
                # self.screen.blit(self.screen_overgame,self.a)

                self.show_go_screen()


    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        for events in pygame.event.get():
            if events.type == QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if events.type == KEYDOWN:
                if events.key == K_LEFT:
                    self.player.runleft = True
                elif events.key == K_RIGHT:
                    self.player.runright = True
                elif events.key == K_a:
                    self.player.jump = True
                elif events.key == K_DOWN:
                    self.player.stand = True
            if events.type == KEYUP:
                if events.key == K_LEFT:
                    self.player.runleft = False
                if events.key == K_RIGHT:
                    self.player.runright = False
                if events.key == K_a:
                    self.player.jump = False

    def draw(self):
        self.screen.blit(self.map.background, self.camera.apply(self.map))
        #self.draw_grid()
        for sprites in self.all_sprites:
            self.screen.blit(sprites.image, self.camera.apply(sprites))
        self.screen.blit(self.total_score,(50,50))
        # self.screen.blit(self.over,(100,100))
        display.flip()

    def draw_grid(self):
        for i in range(0, WIDTH, TILE_SIZE):
            draw.line(self.screen, LIGHT_GREY, (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, TILE_SIZE):
            draw.line(self.screen, LIGHT_GREY, (0, i), (WIDTH, i))

    def show_start_screen(self):
        title = GameMenu(self.screen)
        title.draw_title()


    def show_go_screen(self):
        self.go_screen = GameGO(self.screen)
        return self.go_screen.draw_gameover()

    # def show_over_screen(self)
    #     self.screen.fill(WHITE)
    #     self.text_over = font.SysFont('ActionIsShaded', 50)
    #     self.screen_overgame = self.text_over.render("Game Over",True, (255,0,0))
    #     self.screen.blit(self.screen_overgame,(WIDTH/2,HEIGHT/2))
        

while True:
    game = Main()
    game.show_start_screen()
    while game.running:
        # print game.gameover
        game.new()
        game.run()
        game.running = game.show_go_screen()
quit()