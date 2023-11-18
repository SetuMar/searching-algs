import math
import pygame
from settings import SCREEN_SIZE

class Tile:
    DIMENSIONS = (50, 50)
    
    # default color
    DEFAULT_COLOR = (255, 255, 255)
    # if we have searched this tile already
    SEARCHED_COLOR = (0, 0, 255)
    # if we are currently searching this tile
    SEARCHING_COLOR = (0, 255, 255)
    # start position color
    START_COLOR = (255, 0, 0)
    # end position color
    END_COLOR = (0, 255, 0)
    # color of path
    PATH_COLOR = (255, 255, 0)
    # color of grid
    GRID_COLOR = (100, 100, 100)
    # color of wall
    WALL_COLOR = (0, 0, 0)
    
    def __init__(self, pos:pygame.Vector2) -> None:
        self.rect = pygame.Rect(pos.x, pos.y, Tile.DIMENSIONS[0], Tile.DIMENSIONS[1])
        self.color = Tile.DEFAULT_COLOR
        
        # what tile came to this tile (chained together, they draw the path back)
        self.search_history = []
        
    def draw_walls(self):
        mouse_buttons = pygame.mouse.get_pressed()
        
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if mouse_buttons[0]:
                self.color = Tile.WALL_COLOR
            elif mouse_buttons[2]:
                self.color = Tile.DEFAULT_COLOR
        
    def draw(self, display:pygame.Surface) -> None:
        # draw the rectangle
        pygame.draw.rect(display, self.color, self.rect)
        
    @classmethod
    def draw_grid(cls, display):
        for y in range(0, SCREEN_SIZE[1], cls.DIMENSIONS[1]):
            pygame.draw.line(display, Tile.GRID_COLOR, (0, y), (SCREEN_SIZE[0], y))

        for x in range(0, SCREEN_SIZE[0], cls.DIMENSIONS[0]):
            pygame.draw.line(display, Tile.GRID_COLOR, (x, 0), (x, SCREEN_SIZE[1]))
      
    @classmethod  
    def generate_tiles(cls) -> dict:
        tiles = {}
        
        for y in range(0, SCREEN_SIZE[1], cls.DIMENSIONS[1]):
            for x in range(0, SCREEN_SIZE[0], cls.DIMENSIONS[0]):
                tiles.update({(x / cls.DIMENSIONS[0], y / cls.DIMENSIONS[1]) : cls(pygame.Vector2(x, y))})
                
        return tiles

    @staticmethod
    def update_tiles(tiles:dict, display, sim_started:bool) -> None:
        for t in tiles.values():
            if not sim_started:
                t.draw_walls()
            t.draw(display)