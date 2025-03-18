import pygame
from settings import UI_FONT, UI_FONT_SIZE, UI_BG_COLOR, UI_BORDER_COLOR, TEXT_COLOR

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.options = ["Start Game", "Options", "Exit"]
        self.selected_option = 0
        self.running = True
        self.screen = pygame.display.get_surface()

    def draw(self, surface):
        surface.fill(UI_BG_COLOR)
        for index, option in enumerate(self.options):
            text_surface = self.font.render(option, True, TEXT_COLOR)
            rect = text_surface.get_rect(center=(surface.get_width() // 2, 100 + index * 50))
            if index == self.selected_option:
                pygame.draw.rect(surface, UI_BORDER_COLOR, rect.inflate(20, 10), 2)
            surface.blit(text_surface, rect.topleft)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif keys[pygame.K_DOWN]:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif keys[pygame.K_RETURN]:
            if self.selected_option == 0:
                self.running = False  # Start Game
            elif self.selected_option == 2:
                pygame.quit()
                exit()