import pygame
from utilities import import_csv_layout, import_folder, search_dict
from config import config
from level_data import level, load_level_data
from weapon_data import load_projectile_images
from player_data import load_player_images
from enemy_data import load_enemy_images
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
        level['sprite_groups']['visible_sprites'] = self.visible_sprites = pygame.sprite.Group()
        level['sprite_groups']['obstacle_sprites'] = self.obstacle_sprites = pygame.sprite.Group()
        level['sprite_groups']['entity_sprites'] = self.entity_sprites = pygame.sprite.Group()
        level['sprite_groups']['weapons_sprites'] = self.weapon_group = pygame.sprite.Group()
 
        # Initialize player and level
        self.player = None
        self.level_index = level['level_config']['level_index']
        self.level_name = level['level_config']['level_list'][self.level_index]
        print (f'self.level_name = {self.level_name}')
        
        self.load_all_assets()

        # Initialize controls
        self.controls = controls
    
    def load_all_assets (self):
            load_level_data()
            load_projectile_images()
            load_enemy_images()
            load_player_images()

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

            # First pass: Create floor and walls
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * self.tilesize
                        y = row_index * self.tilesize

                        if style == 'floor':
                            surf = graphics['floor'][int(col)]
                            Tile((x, y), self.visible_sprites, 'floor', surf)
                        elif style == 'wall':
                            surf = graphics['wall'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)

        # Second pass: Create the player FIRST
        for row_index, row in enumerate(layouts['entities']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize
                y = row_index * self.tilesize

                if col == '19':  # Player
                    self.create_player((x, y), [self.visible_sprites,  self.entity_sprites], self.controls)

        # Third pass: Create enemies AFTER the player
        for row_index, row in enumerate(layouts['entities']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize
                y = row_index * self.tilesize

                if col == '29':  # Enemy
                    enemy_name = 'test'
                    self.create_enemy(enemy_name, (x, y), [self.visible_sprites, self.entity_sprites], self.player, 'enemy')
                    '''s
                    Tile((x, y), [self.visible_sprites, self.entity_sprites], 'entities', surf)'''
        
        level['sprite_groups']['visible_sprites'] = self.visible_sprites
        level['sprite_groups']['obstacle_sprites'] = self.obstacle_sprites
        level['sprite_groups']['entity_sprites'] = self.entity_sprites

        print(f"Visible sprites count: {len(self.visible_sprites)}")
        print(f"Entity sprites count: {len(self.entity_sprites)}")

    def create_player(self, pos, groups, controls):
        self.player = Player(pos, groups, controls)
        print(f'Player created at {pos}')


    def create_enemy(self, name, pos, groups, player, sprite_type):
        self.enemy = Enemy(name, pos, groups, player, sprite_type)
        print(f"Enemy '{name}' created at {pos}")