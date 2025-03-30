import pygame
from utilities import import_csv_layout, import_folder, search_dict
from settings import config
from level_data import level, load_level_data
from tile import Tile
from player import Player
from enemy import Enemy

class Game:
    def __init__(self, controls):
        # Initializing screen and surface 
        self.screen = config['screen']['screen']
        self.bg_color = config['ui']['colors']['BG_COLOR']
        self.tilesize = config['screen']['TILESIZE']
        
        # Initialize Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        level['level_config']['visible_sprites'] = self.visible_sprites = pygame.sprite.Group()
        level['level_config']['obstacle_sprites'] = self.obstacle_sprites = pygame.sprite.Group()


        # Initialize player and level
        self.player = None
        self.level_index = level['level_config']['level_index']
        self.level_name = level['level_config']['level_list'][self.level_index]
        print (f'self.level_name = {self.level_name}')
        load_level_data()
        # Initialize controls
        self.controls = controls
    
        
    def create_map(self):
        # Create level counter
        layouts = {
            'floor': level['test_level']['test_floor_layout'],
            'wall': level['test_level']['test_wall_layout'],
            'entities': level['test_level']['test_entity_layout'],
        }
 
        graphics = {
            'floor': level['test_level']['test_graphics'],
            'wall': level['test_level']['test_graphics'],
            'entities': level['test_level']['test_graphics'],
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
                                self.create_enemy(enemy_name, (x, y), [self.visible_sprites, self.obstacle_sprites], self.player, 'enemy')
                                surf = graphics['entities'][int(col)]
                                Tile((x, y), [self.visible_sprites], 'entities', surf)
        
        level['level_config']['visible_sprites'] = self.visible_sprites
        level['level_config']['obstacle_sprites'] = self.obstacle_sprites

    def create_player(self, pos, obstacle_sprites, controls):
        self.player = Player(pos, [self.visible_sprites, self.obstacle_sprites], controls)
        print(f'Player created at {pos}')
        level['level_config']['visible_sprites'] = self.visible_sprites
        level['level_config']['obstacle_sprites'] = self.obstacle_sprites

    def create_enemy(self, name, pos, groups, player, sprite_type):
        self.enemy = Enemy(name, pos, groups, player, sprite_type)
        print(f"Enemy '{name}' created at {pos}")
    

    '''def load_level_data(self, lvl_index):
        """Load the level data from the 'level' dictionary."""
        level_name = f"test_lvl"  # Update with a dynamic level name if necessary
        
        # Load the level data (layout and graphics) from the level dictionary
        self.level_data = level.get(level_name, {})

        self.floor_layout = self.level_data.get('test_floor_layout', [])
        self.wall_layout = self.level_data.get('test_wall_layout', [])
        self.entity_layout = self.level_data.get('test_entity_layout', [])
        self.graphics = self.level_data.get('test_graphics', [])'''
