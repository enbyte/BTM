import pygame
import copy



class Tile:
    def __init__(self, image, x, y):
        if type(image) == str:
            self.image = pygame.image.load(image).convert()
        elif type(image) == pygame.Surface:
            self.image = image
        else:
            print("Unrecognized type of image %s in Tile.__init__()" % type(image))

        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.image.get_width(), self.image.get_height())

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def get_rect(self):
        return self.rect

class Tilemap:
    def __init__(self, matrix, tile_image_list, TILE_SIZE=32):
        self.matrix = matrix
        self.tile_matrix = copy.deepcopy(matrix)
        x, y = 0, 0
        for row in self.tile_matrix:
            for thing in row:
                self.tile_matrix[y][x] = Tile(self.tile_image_list[thing], TILE_SIZE * x, TILE_SIZE * y)   
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
        for i in self.tile_matrix:
            z.extend(i)

        return z

    def move_x(self, amount):
        '''
        Move the tilemap and all of the tiles on the x-axis by a given amount.
        '''
        self.x += amount
        for row in self.tile_matrix:
            for tile in row:
                tile.rect.x += amount

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

    def collision_test(self, rect):
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

    def 

    

    

    


        