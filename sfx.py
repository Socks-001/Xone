import pygame
pygame.init()


sfx = {
    'weapon' : {
        'shot': pygame.mixer.Sound('audio/shot.wav'),
    },
    'entity' : {
        'hit': pygame.mixer.Sound('audio/hit.wav'),
        'death': pygame.mixer.Sound('audio/death.wav')
    },
    'menu' : {
        'menu_move': pygame.mixer.Sound('audio/menu_move.wav'),
        'menu_select': pygame.mixer.Sound('audio/select.wav'),
        'marimba': pygame.mixer.Sound('audio/marimba.wav'),
        'blipSelect' : pygame.mixer.Sound('audio/blipSelect.wav'),

    }
}
