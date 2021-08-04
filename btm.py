import pygame
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

        

class _Tile:
    '''
    Internal class used to represent a specific tile in the world.
    '''
    def __init__(self, tiletype, x, y):
        assert type(tiletype) == Tile
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
                self.tile_matrix[y][x] = _Tile(self.tile_list[thing], TILE_SIZE * x, TILE_SIZE * y)   
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

    def collision_test(self, rect, ignore=[]):
        '''
        For each tile in the tilemap, test if it collides with a given pygame.Rect.
        '''
        hit_list = [] # we gonna murder these tiles
        for x in self.get_list_of_tiles():
            if x.colliderect(rect):
                hit_list.append(x)

        return hit_list



class Player:
    def __init__(self, image, x, y):
        self.image = image if type(image) == pygame.Surface else pygame.image.load(image)
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.xvel = 0
        self.yvel = 0

    def move(self, tilemap, ignore=[]):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.xvel
        hit_list = tilemap.collision_test(self.rect, ignore=ignore)
        for tile in hit_list:
            #if not tile
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

if __name__ ==  '__main__':
    class A: pass
    x=A()
    _sticky_load_image(x)
        