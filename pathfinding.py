import pygame
from config import config
import heapq




def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start, [start]))

    visited = set()

    while open_set:
        _, cost, current, path = heapq.heappop(open_set)

        if current == goal:
            return path[1:]  # Omit starting position

        if current in visited:
            continue
        visited.add(current)

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if grid[ny][nx] == 0:
                    heapq.heappush(open_set, (cost + 1 + heuristic((nx, ny), goal), cost + 1, (nx, ny), path + [(nx, ny)]))
    return []

def make_grid(): 
    level_index = level['level_config']['level_index']
    level_list = level['level_list']
    current_level = level_list[level_index]
    level_data = level[current_level]['wall_data']
    TILESIZE = config['tile_size']
    obstacle_sprites = config['level']['sprite_groups']['obstacle_sprites']
    pathfinding_grid = [[0 for col in range(cols)] for row in range(rows)]

    # Mark obstacles
    for sprite in obstacle_sprites:
        x = sprite.rect.x // TILESIZE
        y = sprite.rect.y // TILESIZE
        pathfinding_grid[y][x] = 1
    level['pathfinding_grid'] = pathfinding_grid
