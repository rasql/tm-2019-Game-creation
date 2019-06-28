import pygame
from pygame.locals import *
import os, sys
from platformer_maps import *


class Map:
    """Create a map for a platformer game."""

    def __init__(self, str):
        self.str = str
        self.table = []
        self.tiles = []
        self.img = None
        self.d = 40

        self.edit_mode = False
        self.insert_mode = False
        self.new_tile = 0

        self.load_table()
        self.load_tile('images/herbe.png')
        self.load_tile('images/terre.png')
        self.load_tile('images/pierre.png')
        self.load_tile('images/triangle.png')
        self.make_grid()
        
        self.make_img()


    def load_tile(self, file):
        """Load a tile image."""
        tile = pygame.image.load(file)
        tile = pygame.transform.scale(tile, (self.d, self.d))
        self.tiles.append(tile)

    def load_table(self):
        """Make a table from the string."""
        self.table = []
        lines = self.str.split()
        for line in lines:
            line = list(map(int, list(line)))
            self.table.append(line)
        
        self.n = len(self.table)
        self.m = len(self.table[0])
        self.size = self.m * self.d, self.n * self.d
        

    def make_img(self):
        BLANC = (255, 255, 255)
        """Make the image from the table."""
        self.img = pygame.Surface((self.m * self.d, self.n * self.d))
        self.img.fill(BLANC)
        self.img.set_colorkey(BLANC)

        for i in range(self.n):
            for j in range(self.m):
                x = self.table[i][j]
                if x > 0:
                    tile = self.tiles[x-1]
                    self.img.blit(tile, ((j * 40), (i * 40)))

    def get_tile_val(self, x, y):
        """Get tile value at position (x, y)."""
        i = int(y // self.d)
        j = int(x // self.d)
        return self.table[i][j] 

    def get_tile_rect(self, x, y):
        """Get tile rect at position (x, y)."""
        return self.get_rect(*self.get_index(x, y))
    

    def get_index(self, x, y):
        """Return index (i, j) from postion (x, y)."""
        i = int(y // self.d)
        j = int(x // self.d)
        return i, j

    def get_rect(self, i, j):
        """Return Rect from index (i, j)."""
        return Rect(j * self.d, i * self.d, self.d, self.d)

    def draw(self):
        """Draw tile map to the screen."""
        App.screen.blit(self.img, (0, 0))
        if self.edit_mode:
            App.screen.blit(self.grid, (0, 0))

    def make_grid(self):
        """Make a red grid do use in EDIT mode."""
        grid = pygame.Surface(self.size)
        grid.set_colorkey(Color('black'))  # makes black transparent

        RED = Color('red')
        x1, y1 = self.size
        for i in range(self.n):
            y = i * self.d
            pygame.draw.line(grid, RED, (0, y), (x1, y), 1)

        for j in range(self.m):
            x = j * self.d
            pygame.draw.line(grid, RED, (x, 0), (x, y1), 1)

        self.grid = grid

    def do_event(self, event):
        """Handle mouse and key events."""
        if event.type == KEYDOWN:
            if event.key == K_e:
                self.edit_mode = not self.edit_mode
                print('edit mode:', self.edit_mode)
            if event.key in (K_0, K_1, K_2, K_4):
                self.new_tile = int(event.unicode)
                print('new tile', self.new_tile)
        if self.edit_mode:
            if event.type == MOUSEBUTTONDOWN:
                self.insert_mode = True
            elif event.type == MOUSEBUTTONUP:
                self.insert_mode = False
            elif event.type == MOUSEMOTION and self.insert_mode:
                i, j = self.get_index(*event.pos)
                self.table[i][j] = self.new_tile
                self.make_img()

class Player:
    """Define a player class."""
    def __init__(self):

        self.w = 40
        self.h = 40
        self.d = 40
        cube = pygame.image.load("images/zombie.png").convert_alpha()
        self.img = pygame.transform.scale(cube, (self.w, self.h))

        self.x = 100
        self.y = 100
        self.vx = 0
        self.vy = 0
        self.gravity = 0.7
        self.speed = 7
        self.on_ground = False
        self.rect = Rect(self.x, self.y, self.w, self.h)
        
        self.map = None

    
    def do_event(self, event):
        """Handle key and mouse events."""
        if event.type == KEYDOWN:
            if event.key in (K_UP, K_w):
                self.vy = -15
                print('jump')
            if event.key in (K_DOWN, K_s) and not self.on_ground:
                self.vy = 25

            if event.key == K_RETURN:
                self.x = 300
                self.y = 100
                self.on_ground = False

    def draw(self):
        """Draw the player to the screen."""
        App.screen.blit(self.img, self.rect)

    def update(self, dt):
        """Update the player movement."""
        key = pygame.key.get_pressed()

        # calculate new speed            
        self.vy += self.gravity
        self.vy = min(self.vy, 10)
        self.vx = (key[K_d] + key[K_RIGHT] - key[K_a] - key[K_LEFT]) * self.speed

        # calculte the new position
        self.x += self.vx
        self.y += self.vy
        self.rect.topleft = self.x, self.y

        # index of topleft corne
        i, j = self.map.get_index(self.x, self.y)

        if self.map.table[i+1][j]:
            # self.x = i*d
            pass

        # if self.map.table
 
        
        # check bottom position
        if self.rect.bottom > self.map.size[1]:
            self.on_ground = True
            self.vy = 0
            self.y = self.map.size[1] - self.h

        
        p = self.rect.bottomleft
        tile = self.check_tile(p)
        if tile:
            self.y = tile.top - self.h
            self.on_ground = True
            self.vy = 0
        
        p = self.rect.bottomright
        tile = self.check_tile(p)
        if tile:
            self.y = tile.top - self.h
            self.on_ground = True
            self.vy = 0

        p = self.rect.topleft
        tile = self.check_tile(p)
        if tile:
            self.y = tile.bottom
            self.vy = 0

        p = self.rect.topright
        tile = self.check_tile(p)
        if tile:
            self.y = tile.bottom
            self.vy = 0


        # if vx > 0:

        

        p = self.rect.topright
        tile = self.check_tile(p)
        if tile:
            self.x = tile.left - self.w - 1

        p = self.rect.topleft
        tile = self.check_tile(p)
        if tile:
            self.x = tile.right

        self.rect.topleft = self.x, self.y


    def check_tile(self, pos):
        """Return False if tile is empty, tile Rect otherwise."""
        if self.map.get_tile_val(*pos):
            return self.map.get_tile_rect(*pos)
        else:
            False


class App:
    """Define the game application class."""
    screen = None

    def __init__(self):
        pygame.init()
        App.screen = pygame.display.set_mode((32*40, 16*40))
        self.running = True
        self.objects = []
    
        self.map = Map(map1b)
        self.player = Player()
        self.player.map = self.map

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == KEYDOWN and event.key in (K_ESCAPE, K_q):
                    self.running = False
                else:
                    self.player.do_event(event)
                    self.map.do_event(event)

            self.player.update(1/60)

            App.screen.fill(Color('black'))
            self.map.draw()
            self.player.draw()     
            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    App().run()