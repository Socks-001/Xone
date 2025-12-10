import pygame

from config import config



def debug(info, x, y):
        # Initialize Variables
        UI_FONT = config['debug']['FONT']
        UI_FONT_SIZE = config['debug']['FONT_SIZE']
        UI_BG_COLOR = config['debug']['colors']['UI_BG']
        UI_BORDER_COLOR = config['debug']['colors']['UI_BORDER_COLOR']
        font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        display_surface = pygame.display.get_surface()
        debug_surf = font.render(str(info),False,'White')
        debug_rect = debug_surf.get_rect(topleft = (x,y))
        pygame.draw.rect(display_surface,UI_BG_COLOR,debug_rect.inflate(6,6))
        pygame.draw.rect(display_surface, UI_BORDER_COLOR, debug_rect.inflate(6,6),2)
        display_surface.blit(debug_surf,debug_rect)

def sprite_group_highlight(sprite_group, surface, color_index, line_width = 2):
    """Draws outlines around all tiles in the sprite group using a selected color."""
    
    # Define the color mapping
    colors = [
        config['debug']['colors']['DEBUG_LINE_COLOR'],      # Blue for wall
        config['debug']['colors']['DEBUG_LINE_COLOR_2'],    # Green for player
        config['debug']['colors']['DEBUG_LINE_COLOR_3'],    # Red for enemy
        config['debug']['colors']['DEBUG_LINE_COLOR_4'],     # Pink for weapon
        config['debug']['colors']['DEBUG_LINE_COLOR_5'],    # Yellow for hitbox
        config['debug']['colors']['DEBUG_LINE_COLOR_6'],     # Orange for special effects
        config['debug']['colors']['DEBUG_LINE_COLOR_7'],    # Purple for special entities

    ]

    # Ensure the color_index is within bounds
    if 0 <= color_index < len(colors):
        selected_color = colors[color_index]
    else:
        selected_color = 'White'  # Default color if index is out of bounds

    # Draw rectangles around the sprites
    for sprite in sprite_group:
        pygame.draw.rect(surface, selected_color, sprite.rect, line_width)  # Outline with 2px thickness
        # Only draw hitbox/projectile_hitbox if they exist
        if hasattr(sprite, 'hitbox') and sprite.hitbox:
            pygame.draw.rect(surface, colors[4], sprite.hitbox, line_width)

        if hasattr(sprite, 'projectile_hitbox') and sprite.projectile_hitbox:
            pygame.draw.rect(surface, colors[4], sprite.projectile_hitbox, line_width)

