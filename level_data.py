import pygame
from utilities import import_csv_layout, import_folder  # Assuming these functions exist

pygame.init()

# Level dictionary to store data
level = {
    'lvl': {
        'game' : None,
        'game_running': True,
        'level_running' : True,
        'visible_sprites' : None,
        'obstacle_sprites' : None,
        'level_index' : 1,
        'level_number' : ['test', 0, 1, 2],
    },

    'test_lvl': {  
        'test_graphics': None,  
        'test_floor_layout': None,
        'test_wall_layout': None,
        'test_entity_layout': None
    },
    'sprite_groups' : {'visible_sprites' : None,
                       'obstacle_sprites' : None
                       }
}

def load_level_data(level_name):
    """Loads level data including floor, walls, and entities."""
    
    # Load CSV layouts
    floor_layout = import_csv_layout(f'level_data/{level_name}/floor.csv')
    level['test_lvl']['test_floor_layout'] = floor_layout
    
    wall_layout = import_csv_layout(f'level_data/{level_name}/wall.csv')
    level['test_lvl']['test_wall_layout'] = wall_layout
    
    entity_layout = import_csv_layout(f'level_data/{level_name}/entities.csv')
    level['test_lvl']['test_entity_layout'] = entity_layout

    # Load graphics
    test_graphics = import_folder('graphics/test')
    level['test_lvl']['test_graphics'] = test_graphics

load_level_data()

