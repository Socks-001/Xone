import pygame
from settings import config
from utilities import search_dict, quit

class Menu:
    def __init__(self):
        
        #Import search util
        self.search_dict = search_dict

        # UI 
        self.font = pygame.font.Font(self.search_dict(config,'UI_FONT')), (self.search_dict(config,'UI_FONT_SIZE'))
        self.text_color = search_dict(config,'TEXT_COLOR')
        self.home_menu = self.search_dict(config,'HOME_MENU')
        self.settings_menu = self.search_dict(config,'SETTINGS_MENU')
        self.pause_menu = self.search_dict(config,'PAUSE_MENU')
        
        # Menu running and Cooldown
        self.running = self.search_dict(config,'menu_running')
        self.can_move = search_dict(config,'can_move')  # Allow movement by default
        self.can_select = True  # Allow selection by default
        self.can_move_time = None
        self.selection_cooldown_time = None
        self.options_list = [self.home_menu, self.settings_menu]  # List of menus
        self.options_selection = self.search_dict(config,'options_selection')  # Initialize selected option for the current menu
        self.selection = self.search_dict(config,'selection')
        self.options = self.options_list[self.options_selection]  # Select the current menu options
        self.cooldown = self.search_dict(config,'COOLDOWN')  # Cooldown time in milliseconds
        self.quit = quit

        # Screen
        self.screen_width = search_dict(config,'SCREEN_Width')
        self.screen_height = self.screen_width = search_dict(config,'SCREEN_HEIGHT')
        self.screen = search_dict(config,'screen') 
        self.scale_factor_list = self.screen_width = search_dict(config,'SCALE_FACTOR_LIST')
        self.scale_factor_index = self.screen_width = search_dict(config,'SCALE_FACTOR_INDEX')
        self.scale_factor = search_dict('scale_factor')

        
       

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
            text_surface = self.font.render(option, False,self.text_color)
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
            