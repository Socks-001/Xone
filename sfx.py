import pygame

sfx = {
    'weapon' : {
        'shot': None,
    },
    'entity' : {
        'hit': None,
        'death': None
    },
    'menu' : {
        'menu_move': None,
        'menu_select': None,
        'marimba': None,
        'blipSelect' : None,

    }
}

def populate_sfx(type, name):
    try:
        sfx_path = f'audio/sfx/{name}.wav'
        sound_effect = pygame.mixer.Sound(sfx_path)
        sfx[type][name] = sound_effect
    except pygame.error as e:
        print(f'Error loading sfx {type}/{name}: {e}')

def load_sfx () : 
    for type in sfx:
        for name in sfx[type]:
            populate_sfx(type, name)
            
