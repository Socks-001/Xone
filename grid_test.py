import pygame
from csv import reader

def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def make_grid():
    """Build a pathfinding grid from current level's obstacle sprites."""
    walls = import_csv_layout(f'level_data/test_level/walls.csv') #csv for current level walls

    grid = []
    for row in walls:
        grid_row = []
        for tile in row:
            if int(tile) == -1:  # Assume -1 means empty/walkable
                grid_row.append(0)
            else:
                grid_row.append(1)  # Any tile with a sprite (wall) is blocked
        grid.append(grid_row)

    for row in grid:
        print(' '.join(str(cell) for cell in row))
    
    return grid

make_grid()
# The above code is a simplified version of the original code, focusing on the grid creation part.