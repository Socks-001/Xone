import pygame

graphics = {
    'player': {
        'sprite': None
    },
    'enemies': {
        'goblin': None,
        'knight': None,
        'skeleton': None,
    },
    'projectiles': {
        'test': None
    }
}

def populate_graphics_images(type, name):
    try:
        image_path = f'graphics/{type}/{name}.png'
        image = pygame.image.load(image_path).convert_alpha()
        graphics[type][name] = image
        print (f'{name} loaded sucessfully')
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
            
