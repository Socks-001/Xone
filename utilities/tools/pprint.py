import pprint 
pp = pprint.PrettyPrinter(depth=6)

config = {
    'screen': {
        'SCREEN_WIDTH': 240,    
        'SCREEN_HEIGHT': 240,
        'FPS': 60,
        'TILESIZE': 16,
        'SCALE_FACTOR_LIST': [1, 2, 4, 6],
        'SCALE_FACTOR_INDEX': 0,
        'SCALE_FACTOR': 1  # Will be updated dynamically
    },

    'ui': {
        'font': 'graphics/font/joystix monospace.otf',
        'font_size': 12,
        'colors': {
            'bg': '#6dc286',
            'water': '#71ddee',
            'ui_bg': '#7ee4ff',
            'ui_border': '#4bb2cd',
            'text': '#fffde4',
            'health': '#dd5929',
            'energy': 'blue',
            'ui_border_active': 'gold',
            'DEBUG_LINE_WIDTH': 10,
            'DEBUG_LINE_COLOR': (200, 30, 10)
        }
    },

    'menu': {
        'home': ['Start Game', 'Options', 'Quit'],
        'settings': ['Volume', 'Scale', 'Fullscreen', 'Back'],
        'pause': ['Resume', 'Options', 'Quit'] 
    }
}

# Dynamically update SCALE_FACTOR based on the index
#config['screen']['SCALE_FACTOR'] = config['screen']['SCALE_FACTOR_LIST'][config['screen']['SCALE_FACTOR_INDEX']]


pprint.pp(config)