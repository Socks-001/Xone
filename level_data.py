#level_data.py
import pygame
from utilities import import_csv_layout, import_folder, load_image_with_proper_alpha, load_named_tile_dict  # Assuming these functions exist
import os


# Level dictionary to store data
level = {
    'level_config': {
        'game' : None,
        'game_running': True,
        'level_running' : True,
        'visible_sprites' : None,
        'obstacle_sprites' : None,
        'level_index' : 0,
        'level_list' : [0, 1, 2]
    },

    'current' : {
        'pathfinding_grid' : None,
        'static_index' : None, 
        'dynamic_index' : None
    },

    'level_0': {  
        'floor_graphics': None,  
        'wall_graphics': None,
        'floor_layout': None,
        'wall_layout': None,
        'entity_layout': None,
        'lights_layout': None,
        'decor_layout': None
    },
    
    'sprite_groups' : {'visible_sprites' : None,
                       'obstacle_sprites' : None,
                       'weapons_sprites' : None,
                       'entity_sprites' : None,
                       'player_sprites' : None,
                       'enemy_sprites' : None,
                       'floor_sprites' : None,
                       'wall_sprites' : None,
                       'decor_sprites' : None,
                       }
}


def load_level_data():
    """Loads level data including floor, walls, and entities."""

    level_index = level['level_config']['level_index']
    # Load CSV layouts
    floor_layout = import_csv_layout(f'level_data/generated/floor.csv')
    wall_layout = import_csv_layout(f'level_data/generated/wall.csv')
    entity_layout = import_csv_layout(f'level_data/generated/entities.csv')
    lights_layout = import_csv_layout(f'level_data/generated/lights.csv')
    decor_layout = import_csv_layout(f'level_data/generated/decor.csv')

    #set dict values
    level[f'level_{level_index}']['floor_layout'] = floor_layout
    level[f'level_{level_index}']['wall_layout'] = wall_layout
    level[f'level_{level_index}']['entity_layout'] = entity_layout
    level[f'level_{level_index}']['lights_layout'] = lights_layout
    level[f'level_{level_index}']['decor_layout'] = decor_layout


