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
        'LOGIC_FPS': 60,
        'TILESIZE': 16,
        'screen': None,
        'fullscreen_trigger': False,
        'scaled_surface': None, 
        'game_surface': None,
    
    },
    
    'debug': {
        'debug': True,  # Set to True to enable debug mode
        'z_test': False,
        'vision_cones': True,
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
        'jump_down': False,
        'jump_pressed_once': False,
        'jump_released': False,
    },
    'physics': {
        'gravity': 0.5,
        'max_step': 4.0
    },
    'ai': {
        'VISION_BASE_DIAMETER': 16,
        'VISION_MIN_RANGE': 8
    },
    'render': {
        'Z_UNIT': 16,
        'CAMERA_Z_OFFSET': 160,
        'Z_SCALE_K': 0.2,
        'Z_REL_STEP': 0.8,
        'CAMERA_Z_SPEED_K': 0.1,
        'CAMERA_Z_MAX': 240,
        'MAX_SCALED_CACHE': 512
    }
}

def add_joystick_buttons(joystick):
    name = joystick.get_name()
    print(f"Detected Controller: {name}")

    # --- Xbox 360 Controller (pygame 2.x) ---
    # Recognized as: "Xbox 360 Controller"
    if "Xbox 360 Controller" in name:
        print("Xbox 360 mapping loaded")
        config['joystick'] = {
            # D-Pad (hat)
            'dpad_up': (0, 1),
            'dpad_down': (0, -1),
            'dpad_left': (-1, 0),
            'dpad_right': (1, 0),

            # Face buttons (mapped into your PS-style action names)
            'x': 0,         # A
            'circle': 1,    # B
            'square': 2,    # X
            'triangle': 3,  # Y

            # Start / Select / Guide
            'share': 6,     # Back
            'start': 7,     # Start
            'ps': 10,       # Guide

            # Thumbstick clicks
            'l_stick_press': 8,
            'r_stick_press': 9,

            # Bumpers
            'l1': 4,
            'r1': 5,

            # Analog axes
            'left_stick_x': 0,   # Axis 0
            'left_stick_y': 1,   # Axis 1
            'right_stick_x': 3,  # Axis 3
            'right_stick_y': 4,  # Axis 4
            'l2_axis': 2,        # Axis 2 (LT)
            'r2_axis': 5         # Axis 5 (RT)
        }

    # --- PlayStation 5 Controller (pygame 2.x) ---
    # Recognized as: "Sony Interactive Entertainment Wireless Controller"
    elif "Sony Interactive Entertainment Wireless Controller" in name:
        print("PS5 mapping loaded")
        config['joystick'] = {
            # D-Pad (hat)
            'dpad_up': (0, 1),
            'dpad_down': (0, -1),
            'dpad_left': (-1, 0),
            'dpad_right': (1, 0),

            # Face Buttons
            'x': 0,         # Cross
            'circle': 1,
            'square': 2,
            'triangle': 3,

            # Share / Options / PS
            'share': 8,
            'start': 9,
            'ps': 10,

            # Thumbstick Clicks
            'l_stick_press': 11,
            'r_stick_press': 12,

            # Bumpers
            'l1': 4,
            'r1': 5,

            # Analog axes
            'left_stick_x': 0,   # Axis 0
            'left_stick_y': 1,   # Axis 1
            'right_stick_x': 3,  # Axis 3
            'right_stick_y': 4,  # Axis 4
            'l2_axis': 2,        # Axis 2
            'r2_axis': 5         # Axis 5
        }

    # --- PS4 Controller ---
    # Name often contains "PS4" or "DualShock"
    elif "PS4" in name or "DualShock" in name:
        print("PS4 mapping loaded")
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

            # Analog Axes
            'left_stick_x': 0,
            'left_stick_y': 1,
            'right_stick_x': 2,
            'right_stick_y': 3,
            'l2_axis': 4,
            'r2_axis': 5
        }

    else:
        # Default to PS4 so the game remains playable
        print("Unknown controller: defaulting to PS4 layout.")
        config['joystick'] = {
            'dpad_up': 11,
            'dpad_down': 12,
            'dpad_left': 13,
            'dpad_right': 14,
            'x': 0,
            'circle': 1,
            'square': 2,
            'triangle': 3,
            'start': 6,
            'share': 4,
            'ps': 5,
            'l_stick_press': 7,
            'r_stick_press': 8,
            'l1': 9,
            'r1': 10,
            'touchpad': 15,
            'left_stick_x': 0,
            'left_stick_y': 1,
            'right_stick_x': 2,
            'right_stick_y': 3,
            'l2_axis': 4,
            'r2_axis': 5
        }


def load_menu_sfx(): 
    config['menu']['menu_select'] = sfx['menu']['menu_select']
    config['menu']['menu_move'] = sfx['menu']['menu_move']
   
