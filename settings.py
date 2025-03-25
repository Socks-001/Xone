# Game Settings Data
import pygame

config = {
    'screen': {
        'SCREEN_WIDTH': 240,    
        'SCREEN_HEIGHT': 240,
        'FPS': 60,
        'TILESIZE': 16,
        'SCALE_FACTOR_LIST': [1, 2, 4, 6],
        'SCALE_FACTOR_INDEX': 0,
        'SCALE_FACTOR': 1,
        'screen' : None,
        'clock' : pygame.time.Clock()
    },

    'ui': {
        'font': 'graphics/font/joystix monospace.otf',
        'font_size': 12,
        'colors': {
            'bg': '#6dc286',
            'water': '#71ddee',
            'UI_BG': '#7ee4ff',
            'UI_BORDER_COLOR': '#4bb2cd',
            'text': '#fffde4',
            'health': '#dd5929',
            'energy': 'blue',
            'UI_BORDER_ACTIVE': 'gold',
            'DEBUG_LINE_WIDTH': 10,
            'DEBUG_LINE_COLOR': (200, 30, 10)
        }
    },

    'menu': {
        'home': ['Start Game', 'Options', 'Quit'],
        'settings': ['Volume', 'Scale', 'Fullscreen', 'Back'],
        'pause': ['Resume', 'Options', 'Quit'], 
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
    'game_running': False,
    'menu_running': True
    },

    'controls' : {
        'controller_found' : False
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
scale_factor = config['screen']['SCALE_FACTOR_LIST'][config['screen']['SCALE_FACTOR_INDEX']]
game_surface = pygame.Surface((config['screen']['SCREEN_WIDTH'] * scale_factor, config['screen']['SCREEN_HEIGHT'] * scale_factor))
config['screen']['game_surface'] = game_surface

#pprint for easier readability