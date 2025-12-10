import pygame
from utilities import import_folder, load_image_with_proper_alpha, load_named_tile_dict

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
        'decor':None
    }
}

def populate_graphics_images(type, name):
    if type != 'level':
        try:
            image_path = f'graphics/{type}/{name}.png'
            image = load_image_with_proper_alpha(image_path)
            graphics[type][name] = image
            print (f'{name} loaded successfully')
        except pygame.error as e:
            print(f'Error loading image {type}/{name}: {e}')

def print_all_graphics():
    for type in graphics:
        print(f"{type}:")
        for name, surface in graphics[type].items():
            print(f"  {name} => {surface}")

def load_graphics () : 
    load_level_graphics()
    for type in graphics:
        for name in graphics[type]:
            populate_graphics_images(type, name)
    

def load_level_graphics():
    floor_graphics_path = f'graphics/level/floor'
    wall_graphics_path = f'graphics/level/wall'
    decor_graphics_path = f'graphics/level/decor'

    # Get list of image filenames in each folder
    floor_files = import_folder(floor_graphics_path, surface = False)
    decor_files = import_folder(decor_graphics_path, surface = False)
    
    # Load them with your function
    graphics[f'level']['floor'] = [
        load_image_with_proper_alpha(image) for image in floor_files
    ]
    graphics[f'level']['decor'] = [
        load_image_with_proper_alpha(image) for image in decor_files
    ]

    graphics[f'level']['wall'] = load_named_tile_dict(
    wall_graphics_path, load_image_with_proper_alpha)
