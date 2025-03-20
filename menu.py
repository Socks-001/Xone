import pygame
from settings import UI_FONT, UI_FONT_SIZE, UI_BG_COLOR, UI_BORDER_COLOR, TEXT_COLOR

class Menu:
    def __init__(self, game, screen_width, screen_height, controls):
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.home_menu = ["Start Game", "self.options", "Quit"]
        self.settings_menu = ["Volume", "Scale", "Fullscreen", "Back"]
        
        self.running = self.game.menu_running  # Initialize running state from game
        self.game = game
        self.controls = controls
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.options_list = (self.home_menu, self.settings_menu)
        self.options_selection = 0  # Initialize selected option for the current menu
        self.selection = 0
       
        
    def draw(self, surface):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        surface.blit(overlay, (0, 0))

        # Draw menu self.options
        self.options = self.options_list[self.options_selection]  # Select the current menu options
        for index, option in enumerate(self.options):
            text_surface = self.font.render(option, True, TEXT_COLOR)
            rect = text_surface.get_rect(center=(surface.get_width() // 2, 100 + index * 25))
            if index == self.selection:
                pygame.draw.rect(surface, UI_BORDER_COLOR, rect.inflate(20, 10), 2)
            surface.blit(text_surface, rect.topleft)

    def update(self):
        #self.running = self.controls.menu_running  # Update menu running state based on controls
        if self.controls.menu_navigation.y == 1:
            self.selection = (self.selection + 1) % len(self.options)
        elif self.controls.menu_navigation.y == -1:
            self.selection = (self.selection - 1) % len(self.options)
        if self.running == 1:
            if self.options == self.home_menu:
                if self.selection == 0:
                    self.running = False  # Start Game
                elif self.selection == 1:
                    self.options_selection = 0  # Go to options menu
                    self.options_selection = 1  # Go to settings menu
                elif self.selection == 2:
                    pygame.quit()
                    exit()
            elif self.options == self.settings_menu:
                if self.selection == 0:
                    pass
                    # Handle volume setting (placeholder)
                elif self.selection == 1: 
                    # Handle scale setting
                    self.game.scale_factor_index = (self.game.scale_factor_index + 1) % len(self.game.scale_factor_list)
                    self.game.scale_factor = self.game.scale_factor_list[self.game.scale_factor_index]
                    self.game.screen = pygame.display.set_mode((self.screen_width * self.game.scale_factor, self.screen_height * self.game.scale_factor))
                elif self.selection == 2:
                    # Handle fullscreen setting (placeholder)
                    pass
                elif self.selection == 3:
                    self.in_settings = False  # Back to main menu
                    self.selection = 1  # Set selection to "self.options"
