Logbook 

def new_features:

    -- create weapon profiles and update the asset loader for all weapon sprites

    -- add ammo to weapon, reload mechanic

    -- 2D lighting 

    -- particle generation

    -- impliment more complex level and map generation

    -- add A* pathfinding

    

def bugs:

    


def Completed:

    -- understand direction and length

    -- fix joystic input (keeps registering as a held button)

    -- load assets dynamically 

    -- store assets dynamically 
    
    -- create entity class (movement and definitions that apply to any entity player, npc, enemy)

    -- basic movement on entity class

    -- impliment health

    -- store attributes for weapons, configuration, enemies in their own dictionary  

    -- create player, enemy, tile class 

    -- add trail to bullets

    -- refactor game_runner name

    -- refactor game_logic name

    -- impliment debug on game_surface

    -- add basic sounds (bullet, hit)

    -- basic level and map generation

    -- basic joystic and keyboard input

    -- fix collision bug , you cant shoot enemies while getting shot

    -- basic collision for walls

    -- basic projectile collision 

    -- advanced projectile collision (tripple raycast, orient bullet to vector, add "accuracy"/shot angle variability)


**Suggested Pathfinding 

GitHub Copilot
To make enemies react to obstacles and navigate around them, you can implement a pathfinding algorithm like A*. This will allow enemies to calculate a path to the player while avoiding obstacles.

Steps to Implement A Pathfinding*
Grid Representation:

Represent the game world as a grid where each cell corresponds to a tile.
Mark cells as walkable or non-walkable based on obstacles.
A Algorithm*:

Use the A* algorithm to calculate the shortest path from the enemy's position to the player's position.
A* uses a combination of:
G-cost: The cost of moving from the start node to the current node.
H-cost: The estimated cost (heuristic) of moving from the current node to the target node.
F-cost: F = G + H.
Path Following:

Once the path is calculated, the enemy moves along the path toward the player.
Implementation
1. Create a Grid Representation
Add a method to generate a grid based on the level layout. Each cell in the grid will represent a tile.


class Game:
    def create_grid(self):
        """Create a grid representation of the level."""
        grid = []
        for y in range(0, self.screen.get_height(), self.tilesize):
            row = []
            for x in range(0, self.screen.get_width(), self.tilesize):
                # Check if the tile is walkable (not an obstacle)
                walkable = True
                for sprite in self.obstacle_sprites:
                    if sprite.rect.collidepoint(x + self.tilesize // 2, y + self.tilesize // 2):
                        walkable = False
                        break
                row.append(walkable)
            grid.append(row)
        return grid

        2. Implement the A Algorithm*
Create a utility function for the A* algorithm.

import heapq

def a_star(grid, start, end):
    """A* pathfinding algorithm."""
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))  # (F-cost, position)
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == end:
            return reconstruct_path(came_from, current)

        neighbors = get_neighbors(current, rows, cols)
        for neighbor in neighbors:
            if not grid[neighbor[1]][neighbor[0]]:  # Skip non-walkable tiles
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                if neighbor not in [item[1] for item in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return []  # Return an empty path if no path is found

def heuristic(a, b):
    """Heuristic function for A* (Manhattan distance)."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, rows, cols):
    """Get valid neighbors for a position."""
    x, y = pos
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < cols and 0 <= ny < rows]

def reconstruct_path(came_from, current):
    """Reconstruct the path from the came_from dictionary."""
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path

    3. Update Enemy Behavior
Modify the Enemy class to use the A* algorithm for pathfinding.

class Enemy(Entity):
    def __init__(self, name, pos, groups, player, sprite_type):
        super().__init__(pos, groups, sprite_type, name)
        self.player = player
        self.path = []  # Store the calculated path
        self.grid = None  # Reference to the grid

    def calculate_path(self):
        """Calculate a path to the player using A*."""
        if not self.grid:
            return

        start = (self.rect.centerx // config['screen']['TILESIZE'], self.rect.centery // config['screen']['TILESIZE'])
        end = (self.player.rect.centerx // config['screen']['TILESIZE'], self.player.rect.centery // config['screen']['TILESIZE'])
        self.path = a_star(self.grid, start, end)

    def follow_path(self):
        """Follow the calculated path."""
        if self.path:
            next_tile = self.path[0]
            next_pos = (next_tile[0] * config['screen']['TILESIZE'], next_tile[1] * config['screen']['TILESIZE'])
            direction = pygame.math.Vector2(next_pos[0] - self.rect.centerx, next_pos[1] - self.rect.centery)
            if direction.length() > 0:
                direction = direction.normalize()
            self.rect.center += direction * self.speed

            # Remove the tile from the path if close enough
            if pygame.math.Vector2(self.rect.center).distance_to(next_pos) < 5:
                self.path.pop(0)

    def update(self):
        """Update enemy behavior."""
        if pygame.time.get_ticks() % 1000 == 0:  # Recalculate path every second
            self.calculate_path()
        self.follow_path()
        self.vulnerability_cooldown()

4. Integrate with the Game
Update the Game class to pass the grid to the enemies.

class Game:
    def create_map(self):
        # Existing map creation logic...
        self.grid = self.create_grid()  # Create the grid

        # Pass the grid to enemies
        for enemy in self.enemy_sprites:
            enemy.grid = self.grid
            
Expected Behavior
Enemies will calculate a path to the player using the A* algorithm.
Enemies will navigate around obstacles to reach the player.
The path will be recalculated periodically to adapt to changes in the player's position.
Let me know if you need further clarification or assistance!

