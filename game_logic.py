import pygame
from utilities import import_csv_layout, import_folder, search_dict
from settings import config
from level_data import level
from tile import Tile
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, controls):
        # Initializing screen and surface 
        self.screen = config['screen']['screen']
        self.bg_color = search_dict(config,'BG_COLOR')
        self.tilesize = search_dict(config,'TILESIZE')
        
        # Initialize Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        config['lvl']['visible_sprites'] = self.visible_sprites = pygame.sprite.Group()
        config['lvl']['obstacle_sprites'] = self.obstacle_sprites = pygame.sprite.Group()


        # Initialize player and level
        self.player = None
        self.level = level['level']['level_index']

        # Initialize controls
        self.controls = controls
    
    def load_level_data(self, lvl_index):
        """Load the level data from the 'level' dictionary."""
        level_name = f"test_lvl"  # Update with a dynamic level name if necessary
        
        # Load the level data (layout and graphics) from the level dictionary
        self.level_data = level.get(level_name, {})

        self.floor_layout = self.level_data.get('test_floor_layout', [])
        self.wall_layout = self.level_data.get('test_wall_layout', [])
        self.entity_layout = self.level_data.get('test_entity_layout', [])
        self.graphics = self.level_data.get('test_graphics', [])
        
    def create_map(self):
        # Create level counter
        layouts = {
            'floor': import_csv_layout(f'level_data/{self.level}/floor.csv'),
            'wall': import_csv_layout(f'level_data/{self.level}/wall.csv'),
            'entities': import_csv_layout(f'level_data/{self.level}/entities.csv'),
        }
 
        graphics = {
            'floor': import_folder('graphics/level'),
            'wall': import_folder('graphics/level'),
            'entities': import_folder('graphics/level'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * self.tilesize
                        y = row_index * self.tilesize

                        if style == 'floor':
                            surf = graphics['floor'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'floor', surf)
                        if style == 'wall':
                            surf = graphics['wall'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)
                        elif style == 'entities':
                            if col == '19':
                                self.create_player((x, y), None, self.controls)
                            if col == '29': 
                                enemy_name = 'test'
                                self.create_enemy(enemy_name, (x, y), [self.visible_sprites, self.obstacle_sprites], self.player)
                                surf = graphics['entities'][int(col)]
                                Tile((x, y), [self.visible_sprites], 'entities', surf)
        
        config['lvl']['visible_sprites'] = self.visible_sprites
        config['lvl']['obstacle_sprites'] = self.obstacle_sprites

    def create_player(self, pos, obstacle_sprites, controls):
        self.player = Player(pos, [self.visible_sprites], self.obstacle_sprites, controls)
        print(f'Player created at {pos}')
        config['lvl']['visible_sprites'] = self.visible_sprites
        config['lvl']['obstacle_sprites'] = self.obstacle_sprites

    def create_enemy(self, name, pos, groups, player):
        self.enemy = Enemy(name, pos, groups, player)
        print(f"Enemy '{name}' created at {pos}")
    
