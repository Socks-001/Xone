import pygame
from settings import UI_FONT, UI_FONT_SIZE, UI_BG_COLOR, UI_BORDER_COLOR, TEXT_COLOR

class Menu:
    def __init__(self, menu_running, screen_width, screen_height):
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.home_menu = ["Start Game", "Options", "Quit"]
        self.settings_menu = ["Volume", "Scale", "Fullscreen", "Back"]
        
        self.running = menu_running
        self.can_move = True  # Allow movement by default
        self.selection_time = None
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.options_list = [self.home_menu, self.settings_menu]  # List of menus
        self.options_selection = 0  # Initialize selected option for the current menu
        self.selection = 0
        self.options = self.options_list[self.options_selection]  # Select the current menu options

    def selection_cooldown(self):
        if not self.can_move:
            current_time = pygame.time.get_ticks()
            if current_time - self.selection_time >= 300:
                self.can_move = True
       
    def draw(self, surface):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        surface.blit(overlay, (0, 0))
        for index, option in enumerate(self.options):
            text_surface = self.font.render(option, True, TEXT_COLOR)
            rect = text_surface.get_rect(center=(surface.get_width() // 2, 100 + index * 25))
            if index == self.selection:
                pygame.draw.rect(surface, UI_BORDER_COLOR, rect.inflate(20, 10), 2)
            surface.blit(text_surface, rect.topleft)

    def input(self, controls):
        if self.running == 1:
            if self.can_move:  # Check if the menu can move
                if controls.menu_navigation.y == 1:
                    self.selection = (self.selection - 1) % len(self.options)
                    self.can_move = False
                    self.selection_time = pygame.time.get_ticks()
                elif controls.menu_navigation.y == -1:
                    self.selection = (self.selection + 1) % len(self.options)
                    self.can_move = False
                    self.selection_time = pygame.time.get_ticks()

    def choose_selection(self):
        if self.options_selection == 0:  # Home menu
            if self.selection == 0:
                self.running = 0  # Start game
            elif self.selection == 1:
                self.options_selection = 1  # Go to settings menu
            elif self.selection == 2:
                print("Quitting game...")
                pygame.quit()
                exit()
        elif self.options_selection == self.settings_menu:
            if self.selection == 0:
                pass # Handle volume setting (placeholder)
            elif self.selection == 1: 
                # Handle scale setting
                self.menu_running.scale_factor_index = (self.menu_running.scale_factor_index + 1) % len(self.menu_running.scale_factor_list)
                self.menu_running.scale_factor = self.menu_running.scale_factor_list[self.menu_running.scale_factor_index]
                self.menu_running.screen = pygame.display.set_mode((self.screen_width * self.menu_running.scale_factor, self.screen_height * self.menu_running.scale_factor))
            elif self.selection == 2:
                # Handle fullscreen setting (placeholder)
                pass
            elif self.selection == 3:
                self.options_selection = 0  # Set selection to "home menu"
                self.selection = 0

    def update(self, controls, game_surface):
        self.input(controls)
        self.selection_cooldown()
        self.draw(game_surface)
        if controls.menu_select:
            self.choose_selection()  # Call the selection function when the button is pressed
            
