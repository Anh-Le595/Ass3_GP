import sys

from os import path
from setting import *
from objects import *

class Game:
    def __init__(self):
        init()
        self.screen = display.set_mode((WIDTH, HEIGHT))
        display.set_caption("game")
        self.clock = time.Clock()

        self.player_image = image.load(path.join(game_path, RUN))
        self.player_image = transform.scale(self.player_image, BLOCK_SIZE)
        self.map = Map(path.join(game_path, MAP_PATH))


    def new(self):
        self.all_sprites = sprite.Group()
        self.ground = sprite.Group()
        self.camera = Camera(self.map.width, self.map.height)
        self.ladder = sprite.Group()

        # read map data
        for layer in self.map.data["layers"]:

            if layer["name"] == "Ground":
                for ground in layer["objects"]:
                    Ground(self, ground)
            if layer["name"] == "Ladder":
                for ladder in layer["objects"]:
                    Ladder(self, ladder)
            if layer["name"] == "Player":
                player = layer["objects"][0]
                self.player = Player(self, player["x"], player["y"])


    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)


    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILE_SIZE):
            draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(GREY)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        display.flip()

    def events(self):
        for e in event.get():
            if e.type == QUIT:
                self.quit()
            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    self.player.runleft = True
                elif e.key == K_RIGHT:
                    self.player.runright = True
                elif e.key == K_a:
                    self.player.jump = True
                elif e.key == K_DOWN:
                    self.player.stand = True
                elif e.key == K_UP:
                    self.player.climb = True
            if e.type == KEYUP:
                if e.key == K_LEFT:
                    self.player.runleft = False
                if e.key == K_RIGHT:
                    self.player.runright = False
                if e.key == K_a:
                    self.player.jump = False
                if e.key == K_UP:
                    self.player.climb = False
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
