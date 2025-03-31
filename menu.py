import pygame
from settings import config
from level_data import level
from utilities import search_dict, quit

class Menu:
    def __init__(self):

        # UI 
        self.font = pygame.font.Font(config['ui']['FONT'], config['ui']['FONT_SIZE'])
        self.text_color = search_dict(config,'TEXT_COLOR')
        self.home_menu = search_dict(config,'HOME_MENU')
        self.settings_menu = search_dict(config,'SETTINGS_MENU')
        self.pause_menu = search_dict(config,'PAUSE_MENU')
        self.UI_BORDER_COLOR = search_dict(config, 'UI_BORDER_COLOR')
        
        # Menu running and Cooldown
        config['menu']['menu_running'] = config['menu']['menu_running']
        self.can_move = True  # Allow movement by default
        self.can_select = True  # Allow selection by default
        self.can_move_time = None
        self.selection_cooldown_time = None
        self.options_lists = [self.home_menu, self.settings_menu]  # List of menus
        self.options_list_index = 0  # Initialize selected option for the current menu
        self.available_options_selection_index = 0
        self.available_options = self.options_lists[self.options_list_index]  # Select the current menu options
        self.cooldown = 300  # Cooldown time in milliseconds
        self.quit = quit

        # Game 
        self.game = level['level_config']['game']

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
        for index, option in enumerate(self.available_options):
            text_surface = self.font.render(option, False,self.text_color)
            rect = text_surface.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2.5 + index * 20))
            if index == self.available_options_selection_index:
                pygame.draw.rect(surface, self.UI_BORDER_COLOR, rect.inflate(20, 10), 2)
            surface.blit(text_surface, rect.topleft)

    def start_game(self):
        config['menu']['menu_running'] = False
        self.game.create_map()

    def reload_menu(self):
        self.available_options = self.options_lists[self.options_list_index]
        

    def input(self, controls):
        if config['menu']['menu_running']:
            if self.can_move:  # Check if the menu can move
                if controls.menu_navigation.y == 1:
                    self.available_options_selection_index = (self.available_options_selection_index + (controls.menu_navigation.y * -1)) % len(self.available_options)
                    self.can_move = False
                    self.can_move_time = pygame.time.get_ticks()
                elif controls.menu_navigation.y == -1:
                    self.available_options_selection_index = (self.available_options_selection_index + (controls.menu_navigation.y * -1)) % len(self.available_options)
                    self.can_move = False
                    self.can_move_time = pygame.time.get_ticks()

    def choose_selection(self):
        if self.can_select:
            if self.options_list_index == 0:  # Home menu
                if self.available_options_selection_index == 0:
                    self.start_game()

                elif self.available_options_selection_index == 1:
                    self.options_list_index = 1
                    self.available_options_selection_index = 1
                    self.reload_menu()

                elif self.available_options_selection_index == 2:
                   self.quit()

            elif self.options_list_index == 1:
                if self.available_options_selection_index == 0:
                    pass # Handle volume setting (placeholder)

                elif self.available_options_selection_index == 1:
                    config['screen']['fullscreen_trigger'] = True

                elif self.available_options_selection_index == 2:
                    self.options_list_index = 0  # Set selection to "home menu"
                    self.available_options_selection_index = 0
                    self.reload_menu()

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
            