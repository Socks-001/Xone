import pygame
from config import config
from level_data import level
from utilities import search_dict, quit
from level_generator import create_csv


class Menu:
    def __init__(self):
        # UI
        self.font = pygame.font.Font(config['ui']['FONT'], config['ui']['FONT_SIZE'])
        self.text_color = search_dict(config, 'TEXT_COLOR')
        self.UI_BORDER_COLOR = search_dict(config, 'UI_BORDER_COLOR')
        self.move_sound = config['menu']['menu_move']
        self.select_sound = config['menu']['menu_select']

        # Menu state
        self.menu_stack = ['HOME_MENU']
        self.menu_running = config['menu']['menu_running']
        self.selection_index = 0
        self.menu_length = len(self.menu_stack[-1])

        # Cooldowns
        self.can_move = True
        self.can_select = True
        self.move_timer = 0
        self.select_timer = 0
        self.cooldown = 300

        # Game ref
        self.game = level['level_config']['game']
        self.game_started = False
        self.quit = quit
        

    def get_current_menu(self):
        self.menu_length = len(config['menu']['menus'][self.menu_stack[-1]]) - 0.5
        return config['menu']['menus'][self.menu_stack[-1]]
        

    def selection_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_move and current_time - self.move_timer > self.cooldown:
            self.can_move = True
        if not self.can_select and current_time - self.select_timer > self.cooldown:
            self.can_select = True

    def draw(self, surface):
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        surface.blit(overlay, (0, 0))

        options = self.get_current_menu()
        for i, (label, _) in enumerate(options):
            text = self.font.render(label, False, self.text_color)
            rect = text.get_rect(center=(surface.get_width() // 2, surface.get_height() // self.menu_length + i * 20))
            if i == self.selection_index:
                pygame.draw.rect(surface, self.UI_BORDER_COLOR, rect.inflate(20, 10), 2)
            surface.blit(text, rect)

    def move_selection(self, direction):
        options = self.get_current_menu()
        self.move_sound.play()
        self.selection_index = (self.selection_index + direction) % len(options)
        self.can_move = False
        self.move_timer = pygame.time.get_ticks()

    def input(self, action_map):
        if not self.menu_running:
            return

        if self.can_move:
            if action_map.get('menu_up'):
                self.move_selection(1)
            elif action_map.get('menu_down'):
                self.move_selection(-1)

        if self.can_select and action_map.get('menu_select'):
            self.choose_selection()
            self.can_select = False
            self.select_timer = pygame.time.get_ticks()

    def choose_selection(self):
        options = self.get_current_menu()
        self.select_sound.play()
        _, action = options[self.selection_index]
        if callable(action):
            action()

    def resume_menu(self):
        config['menu']['menu_running'] = True
        self.menu_running = config['menu']['menu_running']
        self.can_move = True
        self.can_select = True
        self.selection_index = 0
        self.move_timer = 0
        self.select_timer = 0

        # Reset to 'Home Menu'
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            self.selection_index = 0

        print("RESUME MENU CALLED")

    
    def resume_game(self):
        config['menu']['menu_running'] = False
        self.menu_running = config['menu']['menu_running']
        print("RESUME GAME CALLED")

    def update(self, action_map, surface):
        self.input(action_map)
        self.selection_cooldown()
        self.draw(surface)

    # === Actions ===
    def start_game(self):
        config['menu']['menu_running'] = False
        self.menu_running = config['menu']['menu_running']
        create_csv()
        self.game.create_map()
        self.game_started = True
        self.menu_stack = ['PAUSE_MENU']  # Future: resume menu

    def open_settings(self):
        self.menu_stack.append('SETTINGS_MENU')
        self.selection_index = 0

    def back(self):
        if len(self.menu_stack) > 1:
            self.menu_stack.pop()
            self.selection_index = 0

    def toggle_fullscreen(self):
        config['screen']['fullscreen_trigger'] = True
    
    def toggle_debug(self, index):
        if index == 0 :
            config['debug']['debug'] = not config['debug']['debug']
            if config['debug']['debug']:
                print("Debug mode enabled")
            else:
                print("Debug mode disabled")

        if index == 1 : 
            config['debug']['walls_debug'] = not config['debug']['walls_debug']
            walls_debug = config['debug']['walls_debug']
            print(f'weapons_debug = {walls_debug}')
        
        if index == 2 : 
            config['debug']['player_debug'] = not config['debug']['player_debug']
            player_debug = config['debug']['player_debug']
            print(f'weapons_debug = {player_debug}')
        
        if index == 3 : 
            config['debug']['enemies_debug'] = not config['debug']['enemies_debug']
            enemies_debug = config['debug']['enemies_debug']
            print(f'weapons_debug = {enemies_debug}')
        
        if index == 4 :
            config['debug']['weapons_debug'] = not config['debug']['weapons_debug']
            config['debug']['projectile_lines'] = not config['debug']['projectile_lines']
            weapons_debug = config['debug']['weapons_debug']
            print(f'weapons_debug = {weapons_debug}')

            

    def placeholder(self):
        pass
