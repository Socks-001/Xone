import pygame
from utilities import import_csv_layout, search_dict
from config import config
from tile import Tile
from level_data import level
from enemy import Enemy
from graphics_data import graphics
from z_test import ZBounceTest
from player import Player
from player_data import player_data
from light import Light
from light_data import light_types
from pathfinding import make_grid
from spatial_index import ChunkIndex


class Game:
    def __init__(self, controls):
        # Initializing screen and surface 
        self.bg_color = config['ui']['colors']['BG_COLOR']
        self.tilesize = config['screen']['TILESIZE']
        self.game_surface = config['screen']['game_surface']
        
        # Initialize Sprite Groups
        level['sprite_groups']['visible_sprites'] = self.visible_sprites = pygame.sprite.Group()
        level['sprite_groups']['floor_sprites'] = self.floor_sprites = pygame.sprite.Group()
        level['sprite_groups']['wall_sprites'] = self.wall_sprites = pygame.sprite.Group()
        level['sprite_groups']['player_sprites'] = self.player_sprites = pygame.sprite.Group()
        level['sprite_groups']['enemy_sprites'] = self.enemy_sprites = pygame.sprite.Group()
        level['sprite_groups']['obstacle_sprites'] = self.obstacle_sprites = pygame.sprite.Group()
        level['sprite_groups']['entity_sprites'] = self.entity_sprites = pygame.sprite.Group()
        level['sprite_groups']['weapons_sprites'] = self.weapon_group = pygame.sprite.Group()
        level['sprite_groups']['light_sprites'] = self.light_sprites = pygame.sprite.Group()
        level['sprite_groups']['set_dressing_sprites'] = self.set_dressing_sprites = pygame.sprite.Group()
        level['sprite_groups']['dynamic_sprites'] = self.dynamic_sprites = pygame.sprite.Group()

        # Initialize player and level
        self.player = None
        self.level_index = level['level_config']['level_index']
        self.level_list = level['level_config']['level_list']
        self.current_level = f'level_{self.level_list[self.level_index]}'
        #print (f'self.level_name = {self.level_name}')

        # Initialize controls
        self.controls = controls
        self.enemy_gfx = graphics['enemies']
        self.wall_gfx = graphics['level']['wall']
        self.floor_gfx = graphics['level']['floor']
        self.set_dressing_gfx = graphics['level']['set_dressing']

    def collect_visible_tile_blits(self, tilemap, tile_imgs, tilesize, camera_rect, out_list):
        """Fill out_list with (Surface, (x,y)) for visible tiles. Returns out_list."""
        out_list.clear()
        rows = len(tilemap)
        if rows == 0 or not tile_imgs:
            return out_list
        cols = len(tilemap[0])

        # visible tile window (inclusive on right/bottom via -1/+1)
        x0 = max(0, camera_rect.left // tilesize)
        y0 = max(0, camera_rect.top  // tilesize)
        x1 = min(((camera_rect.right  - 1) // tilesize) + 1, cols)
        y1 = min(((camera_rect.bottom - 1) // tilesize) + 1, rows)

        ox, oy = camera_rect.topleft
        append = out_list.append

        for ty in range(y0, y1):
            row = tilemap[ty]
            sy = ty * tilesize - oy
            for tx in range(x0, x1):
                tk = row[tx]
                if tk == "-1":
                    continue
                # clamp index so you don’t crash if you only have 0.png
                idx = int(tk) if tk.isdigit() else 0
                if idx < 0 or idx >= len(tile_imgs):
                    idx = 0
                append((tile_imgs[idx], (tx * tilesize - ox, sy)))
        return out_list


    def _clear_runtime_groups(self):
        # Useful when changing levels / restarting
        for g in (
            self.visible_sprites, self.floor_sprites, self.wall_sprites,
            self.player_sprites, self.enemy_sprites, self.obstacle_sprites,
            self.entity_sprites, self.weapon_group, self.light_sprites, self.set_dressing_sprites, self.dynamic_sprites
        ):
            g.empty()

    def create_map(self):
        
        layouts = {
            'floor': level[self.current_level]['floor_layout'],
            'wall':  level[self.current_level]['wall_layout'],
            'set_dressing': level[self.current_level]['set_dressing_layout'],
            'entities':  level[self.current_level]['entity_layout'],
            'lights':  level[self.current_level]['lights_layout']
        }
 
        graphics = {
            'floor': self.floor_gfx,
            'wall':  self.wall_gfx,
            'entities': self.enemy_gfx,
            'set_dressing': self.set_dressing_gfx
        }

            # First pass: Create floor and walls
        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * self.tilesize + self.tilesize//2
                        y = row_index * self.tilesize + self.tilesize//2


                        if style == 'floor':
                            surf = graphics['floor'][int(col)]
                            Tile((x, y), [self.floor_sprites, self.visible_sprites], 'floor', surf)
                        elif style == 'set_dressing':
                            surf = graphics['set_dressing'][int(col)]
                            Tile((x, y), [ self.set_dressing_sprites, self.visible_sprites], 'set_dressing', surf)
                        elif style == 'wall':
                            surf = graphics['wall'][int(col)]
                            Tile((x, y), [self.wall_sprites, self.visible_sprites, self.obstacle_sprites], 'wall', surf)

        make_grid()
        
        # Second pass: Create the player FIRST
        origin = pygame.Vector2(self.game_surface.get_size()) / 2
        self.create_player((origin), [self.player_sprites, self.visible_sprites,  self.entity_sprites, self.dynamic_sprites], self.controls)
        #print (x,y)
        if self.wall_gfx:
            wall_id = sorted(self.wall_gfx.keys())[0]
            wall_surf = self.wall_gfx[wall_id]
            ZBounceTest(
                (origin.x + 40, origin.y),
                wall_surf,
                [self.visible_sprites, self.dynamic_sprites],
                z_min=0.0,
                z_max=config['render']['Z_UNIT'] * 4,
                z_vel=10.0,
                shadow_surface=wall_surf,
            )

        # Third pass: Create enemies AFTER the player
        for row_index, row in enumerate(layouts['entities']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize + self.tilesize // 2
                y = row_index * self.tilesize + self.tilesize // 2


                if col == '29':  # Enemy
                    enemy_name = 'demos'
                    self.create_enemy(enemy_name, (x, y), [self.enemy_sprites, self.visible_sprites, self.entity_sprites, self.dynamic_sprites],  'enemy')
                    #print (x,y)
        
        # Fourth pass: Create lights 
        for row_index, row in enumerate(layouts['lights']):
            for col_index, col in enumerate(row):
                x = col_index * self.tilesize + self.tilesize//2
                y = row_index * self.tilesize + self.tilesize//2


                if col in light_types:
                    light_config = light_types[col]
                    self.create_light((x, y), [self.visible_sprites, self.light_sprites, self.dynamic_sprites], col)

                '''if col == '50':  # Enemy
                    
                    self.create_light((x, y), [self.visible_sprites, self.light_sprites], 'light', 8)'''
                    
        
        #after tiles/entities created:
        self.static_index = ChunkIndex(self.tilesize, chunk_tiles=16)
        self.dynamic_index = ChunkIndex(self.tilesize, chunk_tiles=16)

        # build static buckets once
        all_static = list(self.floor_sprites) + list(self.wall_sprites) + list(self.set_dressing_sprites)
        self.static_index.build_static(all_static)


        # build dynamic buckets initially
        all_dynamic = list(self.dynamic_sprites) + list(self.weapon_group)
        self.dynamic_index.build_static(all_dynamic)


        level['current']['static_index'] = self.static_index
        level['current']['dynamic_index'] = self.dynamic_index

    def create_player(self, pos, groups, controls):
        self.player = Player(pos, groups, controls)
        player_data['player'] = self.player
        #print(f'Player created at {pos}')

    def create_enemy(self, name, pos, groups, sprite_type):
        self.enemy = Enemy(name, pos, groups, sprite_type)
        #print(f"Enemy '{name}' created at {pos}")
    
    def create_light(self, pos, groups, light_config_index):
        light = Light(pos, groups, light_config_index)
    
    
        

