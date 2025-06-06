import pygame
from utilities import import_csv_layout, import_folder, search_dict
from config import config
from tile import Tile
from level_data import level
from enemy import Enemy
from player import Player
from player_data import player_data
from light import Light
from light_data import light_types
from pathfinding import make_grid



class Game:
    def __init__(self, controls):
        # Initializing screen and surface 
        self.screen = config['screen']['screen']
        self.bg_color = config['ui']['colors']['BG_COLOR']
        self.tilesize = config['screen']['TILESIZE']
        
        # Initialize Sprite Groups
        level['sprite_groups']['visible_sprites'] = self.visible_sprites = pygame.sprite.Group()
        level['sprite_groups']['floor_sprites'] = self.floor_sprites = pygame.sprite.Group()
        level['sprite_groups']['wall_sprites'] = self.wall_sprites = pygame.sprite.Group()
        level['sprite_groups']['player_sprites'] = self.player_sprites = pygame.sprite.Group()
        level['sprite_groups']['enemy_sprites'] = self.enemy_sprites = pygame.sprite.Group()
        level['sprite_groups']['obstacle_sprites'] = self.obstacle_sprites = pygame.sprite.Group()
        level['sprite_groups']['entity_sprites'] = self.entity_sprites = pygame.sprite.Group()
        level['sprite_groups']['weapons_sprites'] = self.weapon_group = pygame.sprite.Group()
        level['sprite_groups']['light_sprites'] = self.light_group = pygame.sprite.Group()
        
        self.update_dicts_refs()

        # Initialize player and level
        self.player = None
        self.level_index = level['level_config']['level_index']
        self.level_list = level['level_config']['level_list']
        self.current_level = self.level_list[self.level_index]
        #print (f'self.level_name = {self.level_name}')

        # Initialize controls
        self.controls = controls


    def update_dicts_refs(self):
            level['sprite_groups']['visible_sprites'] = self.visible_sprites
            level['sprite_groups']['floor_sprites'] = self.floor_sprites
            level['sprite_groups']['wall_sprites'] = self.wall_sprites
            level['sprite_groups']['player_sprites'] = self.player_sprites
            level['sprite_groups']['enemy_sprites'] = self.enemy_sprites
            level['sprite_groups']['obstacle_sprites'] = self.obstacle_sprites
            level['sprite_groups']['entity_sprites'] = self.entity_sprites
            level['sprite_groups']['weapons_sprites'] = self.weapon_group
            level['sprite_groups']['light_sprites'] = self.light_group

    def create_map(self):
        
        layouts = {
            'floor': level[self.current_level]['floor_layout'],
            'wall':  level[self.current_level]['wall_layout'],
            'entities':  level[self.current_level]['entity_layout'],
            'lights':  level[self.current_level]['lights_layout']
        }
 
        graphics = {
            'floor': level[self.current_level]['graphics'],
            'wall':  level[self.current_level]['graphics'],
            'entities': level[self.current_level]['graphics']
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
                            Tile((x, y), [self.floor_sprites, self.visible_sprites], 'floor', surf)
                        elif style == 'wall':
                            surf = graphics['wall'][int(col)]
                            Tile((x, y), [self.wall_sprites, self.visible_sprites, self.obstacle_sprites], 'wall', surf)

        make_grid()
        
        # Second pass: Create the player FIRST
        for row_index, row in enumerate(layouts['entities']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize
                y = row_index * self.tilesize

                if col == '19':  # Player
                    self.create_player((x, y), [self.player_sprites, self.visible_sprites,  self.entity_sprites], self.controls)

        # Third pass: Create enemies AFTER the player
        for row_index, row in enumerate(layouts['entities']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize
                y = row_index * self.tilesize

                if col == '29':  # Enemy
                    enemy_name = 'goblin'
                    self.create_enemy(enemy_name, (x, y), [self.enemy_sprites, self.visible_sprites, self.entity_sprites],  'enemy')
        
        # Fourth pass: Create lights 
        for row_index, row in enumerate(layouts['lights']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize
                y = row_index * self.tilesize

                if col in light_types:
                    light_config = light_types[col]
                    self.create_light((x, y), [self.visible_sprites, self.light_group], col)

                '''if col == '50':  # Enemy
                    
                    self.create_light((x, y), [self.visible_sprites, self.light_group], 'light', 8)'''
                    
        
        self.update_dicts_refs()
       
        print(f"Visible sprites count: {len(self.visible_sprites)}")
        print(f"Entity sprites count: {len(self.entity_sprites)}")

    def create_player(self, pos, groups, controls):
        self.player = Player(pos, groups, controls)
        player_data['player'] = self.player
        print(f'Player created at {pos}')

    def create_enemy(self, name, pos, groups, sprite_type):
        self.enemy = Enemy(name, pos, groups, sprite_type)
        print(f"Enemy '{name}' created at {pos}")
    
    def create_light(self, pos, groups, light_config_index):
        light = Light(pos, groups, light_config_index)
        
