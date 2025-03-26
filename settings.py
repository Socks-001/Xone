# Game Settings Data
import pygame

config = {
    'screen': {
        'SCREEN_WIDTH': 240,    
        'SCREEN_HEIGHT': 240,
        'FPS': 60,
        'TILESIZE': 16,
        'SCALE_FACTOR_LIST': [1, 2, 4, 6],
        'scale_factor_index': 0,
        'scale_surface' : False,
        'screen' : None,
    },

    'ui': {
        'FONT': 'graphics/font/joystix monospace.otf',
        'FONT_SIZE': 12,
        'colors': {
            'BG_COLOR': '#6dc286',
            'WATER_COLOR': '#71ddee',
            'UI_BG': '#7ee4ff',
            'UI_BORDER_COLOR': '#4bb2cd',
            'TEXT_COLOR': '#fffde4',
            'HEALTH_COLOR': '#dd5929',
            'ENERGY_COLOR': 'blue',
            'UI_BORDER_ACTIVE': 'gold',
            'DEBUG_LINE_WIDTH': 10,
            'DEBUG_LINE_COLOR': (200, 30, 10)
        }
    },

    'menu': {
        'HOME_MENU': ['Start Game', 'Options', 'Quit'],
        'SETTINGS_MENU': ['Volume', 'Scale', 'Fullscreen', 'Back'],
        'PAUSE_MENU': ['Resume', 'Options', 'Quit'], 
        'options_selection': 0,
        'selection': 0,
        'COOLDOWN' : 300,
        'menu_running': True,
        'can_move': True,
        'can_select' : True, 
        'can_move_time' : None,
        'selection_cooldown_time' : None
    },

    'lvl': {
    'game_running': True,
    'menu_running': True,
    'lvl_running' : True,
    'create_map' : None
    },

    'controls' : {
        'controller_found' : False,
        'controller_type' : None
    }
     

    }


def add_joystick_buttons(joystick):
    """ Adds joystick button mappings to config['controls'] """
    config['controls'] = {
        
        'dpad_up': joystick.get_button(11),
        'dpad_down': joystick.get_button(12),
        'dpad_left': joystick.get_button(13),
        'dpad_right': joystick.get_button(14),
        'x': joystick.get_button(0),
        'square': joystick.get_button(2),
        'triangle': joystick.get_button(3),
        'circle': joystick.get_button(1),
    }
    print(f"{config['controls']}")

# Directly use the values from the config dictionary
#scale_factor = config['screen']['SCALE_FACTOR_LIST'][config['screen']['SCALE_FACTOR_INDEX']]
#config['screen']['game_surface'] = game_surface

#pprint for easier readability