import pygame

pygame.init()

# Get a list of available fonts
available_fonts = pygame.font.get_fonts()

# Print the fonts
for font in available_fonts:
    print(font)

pygame.quit()