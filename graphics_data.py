import pygame
from utilities import import_folder_paths, load_image_with_proper_alpha, load_named_tile_dict

graphics = {
    'player': {
        'sprite': None
    },
    'enemies': {
        'goblin': None,
        'knight': None,
        'skeleton': None,
        'demos': None,
    },
    'projectiles': {
        'test': None
    },
    'level': {
        'floor': None,
        'wall': None,
        'set_dressing':None
    },
    'particles': {
        'pop': None
    }
}

GRAPHICS_SOURCES = {
    'player': {
        'sprite': ('single', 'graphics/player/sprite.png')
    },
    'enemies': {
        'goblin': ('single', 'graphics/enemies/goblin.png'),
        'knight': ('single', 'graphics/enemies/knight.png'),
        'skeleton': ('single', 'graphics/enemies/skeleton.png'),
        'demos': ('single', 'graphics/enemies/demos.png'),
    },
    'projectiles': {
        'test': ('single', 'graphics/projectiles/test.png')
    },
    'level': {
        'floor': ('folder_list', 'graphics/level/floor'),
        'set_dressing': ('folder_list', 'graphics/level/set_dressing'),
        'wall': ('folder_dict', 'graphics/level/wall')
    },
    'particles': {
        'pop': ('folder_list', 'graphics/pop')
    }
}

def populate_graphics_images(type, name):
    source = GRAPHICS_SOURCES.get(type, {}).get(name)
    if source is None:
        return

    kind, path = source
    try:
        if kind == 'single':
            graphics[type][name] = load_image_with_proper_alpha(path)
        elif kind == 'folder_list':
            files = import_folder_paths(path)
            graphics[type][name] = [load_image_with_proper_alpha(p) for p in files]
        elif kind == 'folder_dict':
            graphics[type][name] = load_named_tile_dict(path, load_image_with_proper_alpha)
    except pygame.error as e:
        print(f'Error loading image {type}/{name}: {e}')

def print_all_graphics():
    for type in graphics:
        print(f"{type}:")
        for name, surface in graphics[type].items():
            print(f"  {name} => {surface}")

def load_graphics () : 
    for type in graphics:
        for name in graphics[type]:
            populate_graphics_images(type, name)

