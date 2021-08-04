import pygame
from pygame.locals import *
import copy
import logging

logging.basicConfig(format='%(levelname)s @ %(asctime)s: %(message)s') # setup logging as example 'WARNING @ 1:32: Bing bong

pygame.init()

_tile_registry = [] # registry of the names of all of the created tiles

def _sticky_load_image(image):
    '''
    If the image is a string, return pygame.image.load() for that image.
    If it is a pygame.Surface, return it.
    Otherwise, throw an error.
    '''
    if type(image) == str:
        return pygame.image.load(image).convert()
    elif type(image) == pygame.Surface:
        return image
    else:
        logging.error('Unrecognized type in _sticky_load_image: %s' % type(image))
        raise TypeError

class Tile:
    '''
    A class to represent a specfic _type_ of tile, i.e. lava, or grass.
    '''
    def __init__(self, image, name=""):
        self.image = _sticky_load_image(image)
        if name == "":
            logging.error('Name cannot be a blank string for a Tile')
            raise NameError
        elif name in _tile_registry:
            logging.error('Name %s for a tile is already in use')
            raise NameError
        else:
            self.name = name
            _tile_registry.append(name)

class NullTile:
    '''
    Class to represent a blank tile with no image and no rect.
    '''
    def __init__(self):
        self.name = ''
    
class _NullTile:
    def draw(self, *pargs, **kwargs):
        pass

        

class _Tile:
    '''
    Internal class used to represent a specific tile in the world.
    '''
    def __init__(self, tiletype, x, y):
        assert type(tiletype) == Tile or type(tiletype) == NullTile
        self.name = tiletype.name
        self.id = tiletype.name #redundancy, used in some Player collisions code
        self.image = tiletype.image
        self.tiletype = tiletype #keep track of it
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect


class Tilemap:
    def __init__(self, matrix, tile_list, TILE_SIZE=32):
        self.matrix = matrix
        self.tile_matrix = copy.deepcopy(matrix)
        x, y = 0, 0
        for row in self.tile_matrix:
            for thing in row:
                if not type(tile_list[thing]) == NullTile:
                    self.tile_matrix[y][x] = _Tile(tile_list[thing], TILE_SIZE * x, TILE_SIZE * y) 
                else:
                    self.tile_matrix[y][x] = _NullTile() 
                x += 1
            x = 0
            y += 1
           
        self.tile_list = tile_list
        self.x = 0
        self.y = 0
    def draw(self, surface):
        '''
        Draw all of the tiles on a given surface.
        '''
        x, y = 0, 0
        for row in self.tile_matrix:
            for tile in row:
                if not type(tile) == _NullTile:
                    tile.draw(surface)

    def get_list_of_tiles(self):
        '''
        Concatenate the entire matrix of tiles into one list, for individual operations on them.
        '''
        z = []
        for row in self.tile_matrix:
            z.extend(row) # add the current row to z

        return z

    def move_x(self, amount):
        '''
        Move the tilemap and all of the tiles on the x-axis by a given amount.
        '''
        self.x += amount
        for row in self.tile_matrix:
            for tile in row:
                tile.rect.x += amount #move each tile's x by a the given amount

    def move_y(self, amount):
        '''
        Move the tilemap and all of the tiles on the y-axis by a given amount.
        '''
        self.y += amount
        for row in self.tile_matrix:
            for tile in row:
                tile.rect.y += amount

    def move_xy(self, xamount, yamount):
        '''
        Move the tilemap and all of the tiles on the x-axis and the y-axis by a given amount.
        '''
        self.move_x(xamount)
        self.move_y(yamount)

    def goto(self, x, y):
        '''
        Move the tilemap and all of the tiles to a given position.
        '''
        x_difference = x - self.x
        y_difference = y - self.y
        self.move_xy(x_difference, y_difference)

    def collision_test(self, rect, ignore_tiletypes=[], ignore_names=[]):
        '''
        For each tile in the tilemap, test if it collides with a given pygame.Rect.
        '''
        hit_list = [] # we gonna murder these tiles
        for x in self.get_list_of_tiles():
            if not type(x) == _NullTile:
                if x.rect.colliderect(rect) and not x.tiletype in ignore_tiletypes and not x.name in ignore_names: # tile x collides with given rect and isn't in the ignore
                    hit_list.append(x.rect)

        return hit_list



class Player:
    def __init__(self, image, x, y):
        self.image = _sticky_load_image(image)
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0

    def move(self, tilemap, ignore_tiletypes=[], ignore_names=[]):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.xvel
        hit_list = tilemap.collision_test(self.rect, ignore_tiletypes=ignore_tiletypes, ignore_names=ignore_names)
        for tile in hit_list:
            if self.xvel > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.xvel < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += self.yvel
        hit_list = tilemap.collision_test(self.rect) #recheck after moving along x-axis
        for tile in hit_list:
            if self.yvel > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.yvel < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return collision_types

    def draw(self, surface):
        surface.blit(self.image, self.rect)

if __name__ ==  '__main__':
    screen = pygame.display.set_mode((19 * 16, 13 * 16), flags=pygame.SCALED)
    running = True
    
    game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]
    dirt = Tile('dirt.png', name="Dirt")
    grass = Tile('grass.png', name="Grass")
    air = NullTile()
    tmap = Tilemap(game_map, {'0': air, '1': dirt, '2': grass}, TILE_SIZE=16)
    p = Player('player.png', 10, 10)
    p.image.set_colorkey((255, 255, 255)) # remove white background
    air_timer = 0
    moving_right, moving_left = False, False
    print("Starting mainloop")
    while running:
        screen.fill((146, 244, 255))
        tmap.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == KEYDOWN:

                if event.key == K_RIGHT:
                    moving_right = True

                if event.key == K_LEFT:
                    moving_left = True

                if event.key == K_UP:
                    if air_timer < 6:
                        p.yvel = -5
                        print("Jump")

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False

                if event.key == K_LEFT:
                    moving_left = False

        xmovement = 0
        if moving_left:
            xmovement -= 2
        if moving_right:
            xmovement += 2

        p.xvel = xmovement


        p.yvel += 0.2
        
        collisions = p.move(tmap)

        if collisions['bottom']:
            p.yvel = 0
            air_timer = 0
        else:
            air_timer += 1

        if collisions['top']:
            p.yvel = 0

        p.draw(screen)

        pygame.display.update()