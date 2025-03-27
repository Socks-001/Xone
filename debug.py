import pygame
pygame.init()
from settings import UI_BG_COLOR, UI_FONT, UI_BORDER_COLOR, UI_FONT_SIZE


font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

def debug(info, x, y):
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(str(info),False,'White')
        debug_rect = debug_surf.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface,UI_BG_COLOR,debug_rect.inflate(6,6))
        pygame.draw.rect(display_surface, UI_BORDER_COLOR, debug_rect.inflate(6,6),2)
        display_surface.blit(debug_surf,debug_rect)

        