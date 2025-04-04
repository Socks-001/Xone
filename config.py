# Game Settings Data
import pygame

config = {
    'screen': {
        'SCREEN_WIDTH': 240,    
        'SCREEN_HEIGHT': 240,
        'FPS': 60,
        'TILESIZE': 16,
        'screen': None,
        'fullscreen_trigger': False,
        'scaled_surface': None, 
        'game_surface': None
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
    'menus': {
        'HOME_MENU': [('Start Game', lambda: config['menu']['menu'].start_game()),
                      ('Options', lambda: config['menu']['menu'].open_settings()),
                      ('Quit', lambda: config['menu']['menu'].quit())],

        'SETTINGS_MENU': [('Volume', lambda: config['menu']['menu'].placeholder()),
                          ('Fullscreen', lambda: config['menu']['menu'].toggle_fullscreen()),
                          ('Back', lambda: config['menu']['menu'].back())],

        'PAUSE_MENU': [('Resume', lambda: config['menu']['menu'].resume_game()),  # Use same as start/resume logic
                       ('Options', lambda: config['menu']['menu'].open_settings()),
                       ('Quit', lambda: config['menu']['menu'].quit())]
    },
    'menu_running': True,
    'selection_cooldown_time': None,
    'menu': None  # You’ll assign the Menu instance here
},

    'controls': {
        'controller_found': False,
        'controller_type': None,
        'dpad_up': None,
        'dpad_down': None,
        'dpad_left': None,
        'dpad_right': None,
        'x': None,
        'square': None,
        'triangle': None,
        'circle': None
    }
}

def add_joystick_buttons(joystick):
    name = joystick.get_name()
    print(f"Detected Controller: {name}")

    if "Xbox" in name:  # Xbox-style controller
        config['joystick'] = {
            'dpad_up': (0, 1),    # Xbox controllers typically use hat switches
            'dpad_down': (0, -1),
            'dpad_left': (-1, 0),
            'dpad_right': (1, 0),
            'x': 2,  # X on Xbox is different from PS4
            'square': 3,  # Equivalent to Y
            'triangle': 4,
            'circle': 1  # Equivalent to B
        }
    elif "PlayStation" in name or "DualShock" in name:  # PS4 controller
        config['joystick'] = {
            'dpad_up': 11,
            'dpad_down': 12,
            'dpad_left': 13,
            'dpad_right': 14,
            'x': 0,  # PS4's X button is 0
            'square': 2,
            'triangle': 3,
            'circle': 1
        }
    else:  # Default if unknown
        print("Unknown joystick detected, using default layout.")
        config['joystick'] = {
            'dpad_up': 11,
            'dpad_down': 12,
            'dpad_left': 13,
            'dpad_right': 14,
            'x': 0,
            'square': 2,
            'triangle': 3,
            'circle': 1
        }