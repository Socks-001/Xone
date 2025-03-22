import pygame
from settings import UI_FONT, UI_FONT_SIZE, UI_BG_COLOR, UI_BORDER_COLOR, TEXT_COLOR, HOME_MENU, SETTINGS_MENU, PAUSE_MENU

class Menu:
    def __init__(self, menu_running, screen, scale_factor_list, scale_factor_index, scale_factor, shared_flags, quit):
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.home_menu = HOME_MENU
        self.settings_menu = SETTINGS_MENU
        self.pause_menu = PAUSE_MENU
        
        self.running = menu_running
        self.can_move = True  # Allow movement by default
        self.can_select = True  # Allow selection by default
        self.can_move_time = None
        self.selection_cooldown_time = None
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen 
        self.scale_factor_list = scale_factor_list
        self.scale_factor_index = scale_factor_index
        self.scale_factor = scale_factor
        self.options_list = [self.home_menu, self.settings_menu]  # List of menus
        self.options_selection = 0  # Initialize selected option for the current menu
        self.selection = 0
        self.options = self.options_list[self.options_selection]  # Select the current menu options
        self.cooldown = 300  # Cooldown time in milliseconds
        self.quit = quit
        self.shared_flags = shared_flags
       

    def selection_cooldown(self):
        if not self.can_move:
            current_time_move = pygame.time.get_ticks()
            if current_time_move - self.can_move_time >= self.cooldown:
                self.can_move = True
        if not self.can_select:
            current_time_selection = pygame.time.get_ticks()
            if current_time_selection - self.selection_cooldown_time >= self.cooldown:
                self.can_select = True
       
    def draw(self, surface):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Black with 50% opacity
        surface.blit(overlay, (0, 0))
        for index, option in enumerate(self.options):
            text_surface = self.font.render(option, False, TEXT_COLOR)
            rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2.5 + index * 20))
            if index == self.selection:
                pygame.draw.rect(surface, UI_BORDER_COLOR, rect.inflate(20, 10), 2)
            surface.blit(text_surface, rect.topleft)

    def start_game(self):
        self.running['menu_running'] = False

    def reload_menu(self):
        self.selection = 0  # reset option to first option
        self.options = self.options_list[self.options_selection]

    def input(self, controls):
        if self.running['menu_running']:
            if self.can_move:  # Check if the menu can move
                if controls.menu_navigation_y == 1:
                    self.selection = (self.selection + (controls.menu_navigation_y * -1)) % len(self.options)
                    self.can_move = False
                    self.can_move_time = pygame.time.get_ticks()
                elif controls.menu_navigation_y == -1:
                    self.selection = (self.selection + (controls.menu_navigation_y * -1)) % len(self.options)
                    self.can_move = False
                    self.can_move_time = pygame.time.get_ticks()

    def choose_selection(self):
        if self.can_select:
            if self.options_selection == 0:  # Home menu
                if self.selection == 0:
                    self.start_game()

                elif self.selection == 1:
                    self.options_selection = 1 # set to settings menu
                    self.reload_menu()

                elif self.selection == 2:
                   self.quit(self)

            elif self.options_selection == 1:
                if self.selection == 0:
                    pass # Handle volume setting (placeholder)

                elif self.selection == 1: 
                    # Handle scale setting
                    self.scale_factor_index = (self.scale_factor_index + 1) % len(self.scale_factor_list)
                    self.scale_factor = self.scale_factor_list[self.scale_factor_index]
                    self.screen = pygame.display.set_mode((self.screen_width * self.scale_factor, self.screen_height * self.scale_factor), pygame.RESIZABLE) 
                    self.shared_flags['reload_surface'] = True
                    
                    print(f'shared flags = {self.shared_flags}')

                elif self.selection == 2:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
                    else:
                        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)

                elif self.selection == 3:
                    self.options_selection = 0  # Set selection to "home menu"
                    self.selection = 0
                    self.options = self.options_list[self.options_selection]
        


    def update(self, controls, game_surface):
        self.input(controls)
        self.selection_cooldown()
        self.draw(game_surface)
        if controls.menu_select:
            #print(f'menu select = {controls.menu_select}')
            self.choose_selection()
            controls.menu_select = 0  # Call the selection function when the button is pressed
            self.can_select = False
            self.selection_cooldown_time = pygame.time.get_ticks()            #print(f'menu select = {controls.menu_select}')
            