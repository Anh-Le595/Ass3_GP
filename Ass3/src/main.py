from os import path
import pygame
from pygame import *
from Objects import *



class Main:
    def __init__(self):
        # init GameWindow, etc
        init()
        self.screen = display.set_mode((WIDTH, HEIGHT))
        display.set_caption(CAPTION)
        self.clock = time.Clock()
        game_path = path.dirname(__file__)
        self.player_image = image.load(path.join(game_path, PLAYER_IMAGE))
        self.map = Map(path.join(game_path, MAP1_PATH), path.join(game_path, BACKGROUND1_PATH))
        self.running = True

    def new(self):
        # start a new game

        # create all sprites
        self.all_sprites = sprite.Group()
        self.ground = sprite.Group()

        for layer in self.map.data["layers"]:
            if layer["name"] == "Ground":
                for ground in layer["objects"]:
                    Ground(self, ground)
            if layer["name"] == "Player":
                self.player = Player(self, layer["objects"][0]["width"], layer["objects"][0]["height"])

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        self.playing = True
        while self.playing :
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()


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
                if events.key == K_RIGHT:
                    self.player.runright = True
                if events.key == K_a:
                    self.player.jump = True
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
        display.flip()

    def draw_grid(self):
        for i in range(0, WIDTH, TILE_SIZE):
            draw.line(self.screen, LIGHT_GREY, (i, 0), (i, HEIGHT))
        for i in range(0, HEIGHT, TILE_SIZE):
            draw.line(self.screen, LIGHT_GREY, (0, i), (WIDTH, i))

    def show_start_screen(self):
        pass
    def show_go_screen(self):
        pass
game = Main()
game.show_start_screen()
while game.running:
    game.new()
    game.run()
    game.show_go_screen()
quit()