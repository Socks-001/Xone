import math
import heapq
from config import config
from level_data import level

def heuristic(a, b, flying=False):
    """Calculate the heuristic distance between two points."""
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return math.sqrt(dx * dx + dy * dy) if flying else max(dx, dy)

def get_neighbors(current, grid, flying=False):
    """Return valid neighbors, preventing diagonal corner clipping unless flying."""
    directions = [
        (-1, 0), (1, 0), (0, -1), (0, 1),     # Cardinal
        (-1, -1), (-1, 1), (1, -1), (1, 1)    # Diagonals
    ]
    
    x, y = current
    rows, cols = len(grid), len(grid[0])
    neighbors = []

    for dx, dy in directions:
        nx, ny = x + dx, y + dy

        if not (0 <= nx < cols and 0 <= ny < rows):
            continue  # Out of bounds

        if grid[ny][nx] != 0:
            continue  # Not walkable

        if dx != 0 and dy != 0 and not flying:
            # Prevent corner clipping: both adjacent sides must be walkable
            if grid[y][ny] != 0 and grid[ny][x] != 0:
                continue

        neighbors.append((nx, ny))

    return neighbors

def astar(grid, start, goal, flying=False):
    """A* pathfinding algorithm with diagonal support and corner clipping prevention."""
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal, flying), 0, start, [start]))
    visited = set()

    while open_set:
        _, cost, current, path = heapq.heappop(open_set)

        if current == goal:
            return path[1:]  # Omit start tile

        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current, grid, flying):
            dx, dy = neighbor[0] - current[0], neighbor[1] - current[1]
            step_cost = math.sqrt(2) if dx != 0 and dy != 0 else 1
            new_cost = cost + step_cost
            priority = new_cost + heuristic(neighbor, goal, flying)
            heapq.heappush(open_set, (priority, new_cost, neighbor, path + [neighbor]))

    return []

def make_grid():
    """Build a pathfinding grid from current level's obstacle sprites."""
    level_index = level['level_config']['level_index']
    level_list = level['level_config']['level_list']
    current_level = level_list[level_index]
    
    TILESIZE = config['screen']['TILESIZE']
    ro = level[current_level]['wall_layout']

    # Assume you know the map size ahead of time or infer it from sprite positions
    max_x = max(sprite.rect.x for sprite in obstacle_sprites) // TILESIZE
    max_y = max(sprite.rect.y for sprite in obstacle_sprites) // TILESIZE
    rows, cols = max_y + 2, max_x + 2  # Add padding

    pathfinding_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    for sprite in obstacle_sprites:
        x = sprite.rect.x // TILESIZE
        y = sprite.rect.y // TILESIZE
        if 0 <= y < rows and 0 <= x < cols:
            pathfinding_grid[y][x] = 1

    level['pathfinding_grid'] = pathfinding_grid

~~~~~~~


    # Calculate dimensions based on level data
    rows = level_data['rows']
    cols = level_data['cols']
    pathfinding_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Mark obstacles
    for sprite in obstacle_sprites:
        x = sprite.rect.x // TILESIZE
        y = sprite.rect.y // TILESIZE
        if 0 <= y < rows and 0 <= x < cols:
            pathfinding_grid[y][x] = 1

    level['pathfinding_grid'] = pathfinding_grid