import math
from grid import Tile
from settings import *

class SortingMethods:
    def __init__(self, start_pos:[int, int], end_pos:[int, int], tiles:dict) -> None:
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        tiles[self.start_pos].color = Tile.START_COLOR
        tiles[self.end_pos].color = Tile.END_COLOR
        
        # indexes which are in need of being searched
        self.tile_indexes_to_search = [start_pos]
        # indexes which have already been searched
        self.searched_indexes = [start_pos]
        self.walls = []
        
        self.path_found = False
        self.path = None
        
        self.tile_edges = (SCREEN_SIZE[0] / Tile.DIMENSIONS[0] - 1, SCREEN_SIZE[1] / Tile.DIMENSIONS[1] - 1)
        
        for v in tiles.values():
            v.search_history = [self.start_pos]
        
        self.tiles_and_distance = {self.start_pos:0}
        
    def breadth_first_search(self, tiles:dict) -> None:
        if not self.path_found:
            next_indexes = []
            
            for t in self.tile_indexes_to_search:
                for y in range(-1, 2):
                    for x in range(-1, 2):
                        if (abs(x + y)) == 1:
                            tile_index_to_search = (t[0] + x, t[1] + y)

                            valid_index = (self.tile_edges[0] >= tile_index_to_search[0] >= 0) and (self.tile_edges[1] >= tile_index_to_search[1] >= 0)
                            if valid_index:
                                if tiles[tile_index_to_search].color == Tile.WALL_COLOR: continue
                                
                                if tile_index_to_search not in self.searched_indexes and tile_index_to_search not in next_indexes:
                                    next_indexes.append(tile_index_to_search)
                                    
                                    tiles[tile_index_to_search].search_history = tiles[t].search_history + [tile_index_to_search]
                                
                                    if tile_index_to_search == self.end_pos:
                                        self.path_found = True
                                        self.path = tiles[tile_index_to_search].search_history
                                        break
                                
                    if self.path_found: break
                
                self.searched_indexes.append(t)
                
                if self.path_found: break
                
            self.tile_indexes_to_search = next_indexes      
                
            for t in self.searched_indexes:
                tiles[t].color = Tile.SEARCHED_COLOR
                
            for t in self.tile_indexes_to_search:
                tiles[t].color = Tile.SEARCHING_COLOR
        else:
            for t in self.path:
                tiles[t].color = Tile.PATH_COLOR
                
        tiles[self.start_pos].color = Tile.START_COLOR
        tiles[self.end_pos].color = Tile.END_COLOR
        
    def dijkstras(self, tiles:dict):
        def calculate_distance(t1, t2):
            return abs(t1[0] - t2[0]) + abs(t1[1] - t2[1])
        
        if not self.path_found:
            # 1. determine the closest tile to the start that hasn't been searched yet
                # this is the parent tile
                
            parent_tile_index = None
            best_tile_dist = math.inf
            
            for t in self.searched_indexes:
                tiles[t].color = Tile.SEARCHED_COLOR
                
            # for t in self.tile_indexes_to_search:
            #     tiles[t].color = Tile.SEARCHING_COLOR
            
            # Inside the loop where you determine the closest tile
            if len(self.searched_indexes) > 1:
                for tile, dist in self.tiles_and_distance.items():
                    if dist < best_tile_dist and tile not in self.searched_indexes:
                        # Introduce tie-breaking based on lexicographical order of coordinates
                        if dist == best_tile_dist:
                            if tile < parent_tile_index:
                                parent_tile_index = tile
                        else:
                            parent_tile_index = tile
                        best_tile_dist = dist
            else:
                parent_tile_index = self.start_pos
                best_tile_dist = 0

                
            # 2. after determining the closest tile, add this to the searched tiles
            self.searched_indexes.append(parent_tile_index)
                
            
            # 3. go around the parent tile in all 4 directions (N, E, S, W)
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if (abs(x) + abs(y)) == 1:
                        tile_index_to_search = (parent_tile_index[0] + x, parent_tile_index[1] + y)

                        valid_index = (self.tile_edges[0] >= tile_index_to_search[0] >= 0) and (self.tile_edges[1] >= tile_index_to_search[1] >= 0)

                        if valid_index:
                            
                            if tiles[tile_index_to_search].color == Tile.WALL_COLOR:
                                self.searched_indexes.append(tile_index_to_search)
                                self.walls.append(tile_index_to_search)
                                self.tiles_and_distance.update({tile_index_to_search:math.inf})
                                continue
                            
                            if tile_index_to_search not in self.searched_indexes: 
                                tiles[tile_index_to_search].color = Tile.SEARCHING_COLOR
                                if tile_index_to_search == self.end_pos:
                                    self.path_found = True
                                    self.path = tiles[parent_tile_index].search_history + [tile_index_to_search]
                                    break
                                
                                distance = calculate_distance(tile_index_to_search, self.end_pos)
                                
                                self.tiles_and_distance.update(
                                    {tile_index_to_search:distance}
                                )
                                
                                tiles[tile_index_to_search].search_history = tiles[parent_tile_index].search_history + [tile_index_to_search]
                                
                                # get distance between search tile and all the starting search tile
                    
                if self.path_found: break
        else:
            for t in self.path:
                tiles[t].color = Tile.PATH_COLOR
                
        tiles[self.start_pos].color = Tile.START_COLOR
        tiles[self.end_pos].color = Tile.END_COLOR
        
        for t in self.walls:
            tiles[t].color = Tile.WALL_COLOR