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

    def draw()


        