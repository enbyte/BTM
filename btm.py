import pygame
from pygame.locals import *
import copy
import logging
import tools

logging.basicConfig(format='%(levelname)s @ %(asctime)s: %(message)s') # setup logging as 'WARNING @ 1:32: Bing bong'

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
    def __init__(self, image, name="", size=32):
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
        self.has_rect = True
        self.size = size

class NullTile:
    '''
    Class to represent a blank tile with no image and no rect.
    '''
    def __init__(self):
        self.name = 'NullTile'
        self.image = pygame.Surface((0, 0))
        self.has_rect = False
        self.size = 0


        

class _Tile:
    '''
    Internal class used to represent a specific tile in the world.
    '''
    def __init__(self, tiletype, x, y):
        assert type(tiletype) == Tile or type(tiletype) == NullTile
        self.name = tiletype.name
        self.image = tiletype.image
        self.tiletype = tiletype #keep track of it
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())
        self.has_rect = tiletype.has_rect

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

    def generate_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)


    def update_tiletype(self, new_tiletype):
        self.tiletype = new_tiletype
        self.image = new_tiletype.image
        self.name = new_tiletype.name
        self.size = new_tiletype.size
        if not self.has_rect and new_tiletype.has_rect: # was a nulltile, converting to a tile
            self.generate_rect()
        elif self.has_rect and not new_tiletype.has_rect: # converting to nulltile
            self.rect.width = 0
            self.rect.height = 0
        self.has_rect = new_tiletype.has_rect
        print("Done with update_tiletype")


class Tilemap:
    def __init__(self, matrix, tile_list, TILE_SIZE=32):
        self.matrix = matrix
        self.TILE_SIZE = TILE_SIZE
        self.tile_matrix = copy.deepcopy(matrix)
        x, y = 0, 0
        for row in self.tile_matrix:
            for thing in row:
                self.tile_matrix[y][x] = _Tile(tile_list[thing], TILE_SIZE * x, TILE_SIZE * y) 
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

    def collision_test(self, rect, ignore_tiletypes=[], ignore_names=[]):
        '''
        For each tile in the tilemap, test if it collides with a given pygame.Rect.
        '''
        hit_list = [] # we gonna murder these tiles
        for x in self.get_list_of_tiles():
            if x.rect.colliderect(rect):
                if x.tiletype in ignore_tiletypes: continue
                if x.name in ignore_names: continue
                hit_list.append(x)
        hit_list = [x for x in hit_list if x.name not in ignore_names and x.tiletype not in ignore_tiletypes]
        return hit_list

    def get_tile_at(self, x, y):
        '''
        Return the tile at x, y in worldspace
        '''
        ydiff = y - self.y
        xdiff = x - self.x
        print("Diff:", xdiff, ydiff)
        ytile = ydiff // self.TILE_SIZE
        xtile = xdiff // self.TILE_SIZE
        print("Tile:", xtile, ytile)
        print("Matrix size:", len(self.tile_matrix), len(self.tile_matrix[0]))
        z = self.tile_matrix[ytile]
        return z[xtile]

    def get_names(self):
        return [x.name for x in self.tile_list]

    def get_tile(self, name):
        for x in self.tile_list:
            if x.name == name:
                return x

    def get_matrix(self):
        '''
        Get the non-tile matrix, with the numbers or whatever.
        '''
        z = tools.matrix(0, len(self.tile_matrix[0]),  len(self.tile_matrix))
        x, y = 0, 0
        for i in z:
            for p in i:
                print('y, x:', y, x)
                t = self.get_tile(self.tile_matrix[y][x].name)
                z[y][x] = self.tile_list.index(t)
                x += 1
            x = 0
            y += 1

        return z



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
        '''
        Move the player, with the velocity member attributes and the tilemap to collide with.
        :param self Duh
        :param tilemap Tilemap to collide with
        :param ignore_tiletypes a list of tiletypes that the player should ignore and not collide with.
        :param ignore_names same, except with names.
        '''
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        self.rect.x += self.xvel
        hit_list = tilemap.collision_test(self.rect, ignore_tiletypes=ignore_tiletypes, ignore_names=ignore_names)
        for t in hit_list:
            tile = t.rect
            if self.xvel > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.xvel < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += self.yvel
        hit_list = tilemap.collision_test(self.rect, ignore_tiletypes=ignore_tiletypes, ignore_names=ignore_names) #recheck after moving along x-axis
        for t in hit_list:
            tile = t.rect
            if self.yvel > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif self.yvel < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
        return collision_types

    def draw(self, surface):
        '''
        Draw the player on a given surface
        '''
        surface.blit(self.image, self.rect)

if __name__ ==  '__main__':
    screen = pygame.Surface((19 * 16, 13 * 16))
    DISPLAY = pygame.display.set_mode((19 * 16, 13 * 16))
    running = True
    TILE_SIZE = 16
    clock = pygame.time.Clock()
    game_map = tools.load_mat('level')
    dirt = Tile('dirt.png', name="Dirt", size=TILE_SIZE)
    grass = Tile('grass.png', name="Grass", size=TILE_SIZE)
    air = NullTile()
    tmap = Tilemap(game_map, [air, dirt, grass], TILE_SIZE=TILE_SIZE)
    p = Player('player.png', 10, 10)
    p.image.set_colorkey((255, 255, 255)) # remove white background
    air_timer = 0
    tot_fps = 0
    num_frames = 1
    to_draw = grass
    moving_right, moving_left = False, False
    print("Starting mainloop")
    font = pygame.font.Font(None, 24)
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
                        #print("Jump")

                if event.key == K_SPACE:
                    tmap.move_x(5)

                if event.key == K_0:
                    to_draw = air
                
                if event.key == K_1:
                    to_draw = grass

                if event.key == K_2:
                    to_draw = dirt

                if event.key == K_s:
                    tools.save(tmap.get_matrix(), input("Filename: "))

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    moving_right = False

                if event.key == K_LEFT:
                    moving_left = False
            if event.type == MOUSEBUTTONDOWN:
                t = tmap.get_tile(*pygame.mouse.get_pos())
                t.update_tiletype(to_draw)

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
        DISPLAY.blit(screen, (0, 0))
        tot_fps += round(clock.get_fps())
        avg = round(tot_fps / num_frames)
        num_frames += 1
        if num_frames > 10**10: #reset every million frames
            num_frames = 1
            tot_fps = 0
        fps = "Average FPS: " + str(avg)
        DISPLAY.blit(font.render(fps, True, (0, 0, 0)), (0, 0))

        pygame.display.update()

        clock.tick()
