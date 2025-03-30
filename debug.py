import pygame
pygame.init()
from settings import config



def debug(info, x, y):
        # Initialize Variables
        UI_FONT = config['ui']['FONT']
        UI_FONT_SIZE = config['ui']['FONT_SIZE']
        UI_BG_COLOR = config['ui']['colors']['UI_BG']
        UI_BORDER_COLOR = config['ui']['colors']['UI_BORDER_COLOR']
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(str(info),False,'White')
        debug_rect = debug_surf.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface,UI_BG_COLOR,debug_rect.inflate(6,6))
        pygame.draw.rect(display_surface, UI_BORDER_COLOR, debug_rect.inflate(6,6),2)
        display_surface.blit(debug_surf,debug_rect)

        