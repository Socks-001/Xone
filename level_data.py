import pygame
from utilities import import_csv_layout, import_folder  # Assuming these functions exist



# Level dictionary to store data
level = {
    'level_config': {
        'game' : None,
        'game_running': True,
        'level_running' : True,
        'visible_sprites' : None,
        'obstacle_sprites' : None,
        'level_index' : 0,
        'level_list' : ['test_level', 0, 1, 2]
    },

    'test_level': {  
        'test_graphics': None,  
        'test_floor_layout': None,
        'test_wall_layout': None,
        'test_entity_layout': None
    },
    'sprite_groups' : {'visible_sprites' : None,
                       'obstacle_sprites' : None,
                       'weapons_sprites' : None,
                       'entity_sprites' : None,
                       'player_sprites' : None,
                       'enemy_sprites' : None,
                       'floor_sprites' : None,
                       'wall_sprites' : None,
                       }
}

def load_level_data():
    """Loads level data including floor, walls, and entities."""
    
    # Load CSV layouts
    floor_layout = import_csv_layout(f'level_data/test_level/floor.csv')
    level['test_level']['test_floor_layout'] = floor_layout
    
    wall_layout = import_csv_layout(f'level_data/test_level/walls.csv')
    level['test_level']['test_wall_layout'] = wall_layout
    
    entity_layout = import_csv_layout(f'level_data/test_level/entities.csv')
    level['test_level']['test_entity_layout'] = entity_layout

    lights_layout = import_csv_layout(f'level_data/test_level/lights.csv')
    level['test_level']['test_lights_layout'] = lights_layout

    # Load graphics and apply convert_alpha to each surface
    raw_graphics = import_folder('graphics/test_level')
    test_graphics = [image.convert_alpha() for image in raw_graphics]  # Apply convert_alpha to each surface
    level['test_level']['test_graphics'] = test_graphics





