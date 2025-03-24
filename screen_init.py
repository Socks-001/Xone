import pygame
from settings import config
from utilities import search_dict

def initialize_screen():
    pygame.init()
    scale_factor = search_dict('SCALE_FACTOR_LIST')[search_dict('SCALE_FACTOR_INDEX')]
    screen = pygame.display.set_mode(search_dict('SCREEN_WIDTH') * scale_factor, config (search_dict('SCREEN_HEIGHT') * scale_factor), pygame.RESIZABLE)
    config['screen']['screen'] = screen
    game_surface = pygame.Surface(search_dict('SCREEN_WIDTH') * scale_factor, config (search_dict('SCREEN_HEIGHT') * scale_factor))
    config['screen']['game_surface'] = game_surface 