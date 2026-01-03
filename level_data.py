#level_data.py
import pygame
from utilities import import_csv_layout, load_image_with_proper_alpha, load_named_tile_dict  # Assuming these functions exist
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
        'dynamic_index' : None,
        'ground_z': 0.0,
        'floor_surface': None,
        'floor_surface_cache': {},
        'floor2_surface': None,
        'floor2_surface_cache': {}
    },

    'level_0': {  
        'floor_graphics': None,  
        'wall_graphics': None,
        'floor_layout': None,
        'floor2_layout': None,
        'wall_layout': None,
        'wall2_layout': None,
        'entity_layout': None,
        'lights_layout': None,
        'set_dressing_layout': None
    },
    
    'sprite_groups' : {'visible_sprites' : None,
                       'obstacle_sprites' : None,
                       'weapons_sprites' : None,
                       'entity_sprites' : None,
                       'player_sprites' : None,
                       'enemy_sprites' : None,
                       'floor_sprites' : None,
                       'wall_sprites' : None,
                       'set_dressing_sprites' : None,
                       'dynamic_sprites' : None
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
    set_dressing_layout = import_csv_layout(f'level_data/generated/set_dressing.csv')
    floor2_path = f'level_data/generated/floor2.csv'
    wall2_path = f'level_data/generated/wall2.csv'
    if os.path.exists(floor2_path):
        floor2_layout = import_csv_layout(floor2_path)
    else:
        floor2_layout = [["-1" for _ in row] for row in floor_layout]
    if os.path.exists(wall2_path):
        wall2_layout = import_csv_layout(wall2_path)
    else:
        wall2_layout = [["-1" for _ in row] for row in wall_layout]

    #set dict values
    level[f'level_{level_index}']['floor_layout'] = floor_layout
    level[f'level_{level_index}']['floor2_layout'] = floor2_layout
    level[f'level_{level_index}']['wall_layout'] = wall_layout
    level[f'level_{level_index}']['wall2_layout'] = wall2_layout
    level[f'level_{level_index}']['entity_layout'] = entity_layout
    level[f'level_{level_index}']['lights_layout'] = lights_layout
    level[f'level_{level_index}']['set_dressing_layout'] = set_dressing_layout



