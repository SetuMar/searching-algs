import pygame
import sys

from grid import Tile
from sort import SortingMethods

from settings import *

import time
import timerglobal

pygame.init()

display = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

tiles = Tile.generate_tiles()
sorter = SortingMethods((4, 4), (15, 9), tiles)

prev_time = time.time()

simulation_timer = timerglobal.Timer(0.05)

start_sim = False

while True:
    display.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                start_sim = True
    
    if simulation_timer.time_check() and start_sim:
        sorter.dijkstras(tiles)
            
        # sorter.breadth_first_search(tiles)

    Tile.update_tiles(tiles, display, start_sim)
    Tile.draw_grid(display)

    current_time = time.time()
    # current time

    difference = current_time - prev_time
    # difference between current time and the previous time measured

    delay = max(1.0 / FPS - difference, 0)
    # check if we need to wait to ensure 60 FPS

    time.sleep(delay)
    # wait the delay

    calculated_fps = 1.0 / (delay + difference)
    # the FPS we have calculated

    prev_time = current_time
    # set previous time to current time

    pygame.display.set_caption("FRAME RATE: " + str(int(calculated_fps)))
    # update the caption

    pygame.display.update()
    clock.tick(FPS)
    # update the display