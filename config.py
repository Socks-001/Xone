# Game Settings Data
from sfx import sfx

config = {
    'color_list' : {
        #debug colors

        # basic colors
        'yellow': (255, 255, 100),
        'blue': (100, 100, 255),
        'red': (255, 100, 100),
        'green': (100, 255, 100),
        'off_white': (255, 255, 200),
        'purple': (69, 54, 99),
        
        # game pallette
        'black': (0, 0, 0),
        'steel_blue': (70, 130, 180),
        'dark_olive': (85, 107, 47),
        'rust': (183, 65, 14),
        'brass': (181, 166, 66),
        'gunmetal': (42, 52, 57),
        'charcoal': (54, 69, 79),
        'sepia': (112, 66, 20),
        'ivory': (255, 255, 240),
        'neon_green':(57, 255, 20)
    },
    
    'screen': {
        'SCREEN_WIDTH': 512,    
        'SCREEN_HEIGHT': 256,
        'FPS': 1200,
        'TILESIZE': 16,
        'screen': None,
        'fullscreen_trigger': False,
        'scaled_surface': None, 
        'game_surface': None,
    
    },
    
    'debug': {
        'debug': True,  # Set to True to enable debug mode
        'DEBUG_LINE_WIDTH': 10,
        'walls_debug' : True,
        'player_debug' : True,
        'enemies_debug' : True, 
        'weapons_debug' : True,
        'projectile_lines' : True,
        'colors': {
        'DEBUG_LINE_COLOR': (0, 0, 255), # Blue for wall
        'DEBUG_LINE_COLOR_2': (0, 255, 0), # Green for player
        'DEBUG_LINE_COLOR_3': (255, 0, 0),  # Red for enemy
        'DEBUG_LINE_COLOR_4': (250, 20, 190),  # Pink for weapon
        'DEBUG_LINE_COLOR_5': (255, 255, 0),  # Yellow for hitbox
        'DEBUG_LINE_COLOR_6': (255, 165, 0),  # Orange for special effects
        'DEBUG_LINE_COLOR_7': (128, 0, 128)}  # Purple for special entities
        
    },
    'ui': {
        'FONT': 'graphics/font/joystix monospace.otf',
        'FONT_SIZE': 12,
        'colors': {
            'BG_COLOR': '#000000',
            'WATER_COLOR': '#71ddee',
            'UI_BG': '#7ee4ff',
            'UI_BORDER_COLOR': '#4bb2cd',
            'TEXT_COLOR': '#fffde4',
            'HEALTH_COLOR': '#dd5929',
            'ENERGY_COLOR': 'blue',
            'UI_BORDER_ACTIVE': 'gold'}
    },

   'menu': {
        'menus': {
            'HOME_MENU': [('Start Game', lambda: config['menu']['menu'].start_game()), 
                        ('Options', lambda: config['menu']['menu'].open_settings()),
                        ('Quit', lambda: config['menu']['menu'].quit())],

            'SETTINGS_MENU': [('Volume', lambda: config['menu']['menu'].placeholder()),
                            ('Fullscreen', lambda: config['menu']['menu'].toggle_fullscreen()),
                            ('Debug', lambda: config['menu']['menu'].toggle_debug(0)),
                            ('walls', lambda: config['menu']['menu'].toggle_debug(1)),
                            ('player', lambda: config['menu']['menu'].toggle_debug(2)),
                            ('enemies', lambda: config['menu']['menu'].toggle_debug(3)),
                            ('weapons', lambda: config['menu']['menu'].toggle_debug(4)),
                            ('Back', lambda: config['menu']['menu'].back())],

            'PAUSE_MENU': [('Resume', lambda: config['menu']['menu'].resume_game()),  # Use same as start/resume logic
                        ('Options', lambda: config['menu']['menu'].open_settings()),
                        ('Quit', lambda: config['menu']['menu'].quit())]
        },
        'menu_running': True,
        'selection_cooldown_time': None,
        'menu': None,  # You’ll assign the Menu instance here
        'menu_select' :None,
        'menu_move' : None,
    },
    'audio' : {
        'music_volume': 0.5,
        'sfx_volume': 0.7
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
        'circle': None,
        'start': None,     
        'share': None,
        'ps': None,        
        'l_stick_press': None,
        'r_stick_press': None,
        'l1': None,
        'r1': None,
        'touchpad': None,
        'left_stick_x': None,  
        'left_stick_y': None,  
        'right_stick_x': None, 
        'right_stick_y': None, 
        'l2_axis': None,       
        'r2_axis': None, 
        'mouse_angle': 0.0,
        'aim_vec': (0.0, 1.0),   # normalized (x, y)
        'fire_down': False,
        'fire_pressed_once': False,
        'fire_released': False,
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

    elif "PS4" in name or "DualShock" in name:  # PS4 controller
        print("PS4 Input Loaded")
        config['joystick'] = {
        # D-Pad (digital)
        'dpad_up': 11,
        'dpad_down': 12,
        'dpad_left': 13,
        'dpad_right': 14,

        # Face Buttons
        'x': 0,         # Cross
        'circle': 1,
        'square': 2,
        'triangle': 3,

        # Start / Options
        'start': 6,     # Options
        'share': 4,
        'ps': 5,        # PS button

        # Thumbstick Clicks
        'l_stick_press': 7,
        'r_stick_press': 8,

        # Bumpers
        'l1': 9,
        'r1': 10,

        # Touchpad
        'touchpad': 15,

        # Analog Axes (these are accessed differently, not as buttons)
        'left_stick_x': 0,  # Axis 0
        'left_stick_y': 1,  # Axis 1
        'right_stick_x': 2, # Axis 2
        'right_stick_y': 3, # Axis 3
        'l2_axis': 4,       # Left Trigger (analog)
        'r2_axis': 5        # Right Trigger (analog)
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

def load_menu_sfx(): 
    config['menu']['menu_select'] = sfx['menu']['menu_select']
    config['menu']['menu_move'] = sfx['menu']['menu_move']
   