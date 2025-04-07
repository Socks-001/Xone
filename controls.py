import pygame
from utilities import search_dict
from config import config, add_joystick_buttons

class Controls:
    def __init__(self):
        pygame.joystick.init()
        self.controller_1 = None
        self.dpad_input_player1 = (0, 0)
        self.button_input_player1 = 0
        self.direction = pygame.math.Vector2()
        self.shoot_direction = pygame.math.Vector2()
        self.menu_navigation = pygame.math.Vector2()
        self.menu_select = 0  # Initialize menu selection state

        # Cooldown for the start button
        self.button_cooldown = 1000  # Cooldown in milliseconds (e.g., 500ms)
        self.can_press_start = True  # Last time the start button was pressed
        self.start_time = 0  # Initialize the last press time


        # Initialize joysticks
        try:
            if pygame.joystick.get_count() > 0:
                self.controller_1 = pygame.joystick.Joystick(0)
                self.controller_1.init()
                print(f"Joystick found: {self.controller_1.get_name()}")
                add_joystick_buttons(self.controller_1)
                self._load_joystick_config()
            else:
                print("No joystick found")
                
        except pygame.error as e:
            print(f"Joystick initialization failed: {e}")

    def _load_joystick_config(self):
        self.dpad_up = search_dict(config, 'dpad_up')
        self.dpad_down = search_dict(config, 'dpad_down')
        self.dpad_left = search_dict(config, 'dpad_left')
        self.dpad_right = search_dict(config, 'dpad_right')
        self.start = search_dict(config, 'start')
        self.x = search_dict(config, 'x')  
        self.square = search_dict(config, 'square')
        self.triangle = search_dict(config, 'triangle')
        self.circle = search_dict(config, 'circle')

    def get_action_map(self):
        if self.menu_navigation != (0, 0):
            print(f'Menu nav = {self.menu_navigation}')
        return {
            'menu_up': self.menu_navigation.y == -1,
            'menu_down': self.menu_navigation.y == 1,
            'menu_select': self.menu_select == 1,
            # Add other mappings as needed (like 'pause', etc.)
        }
    
    def start_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_press_start and current_time - self.start_time > self.button_cooldown:
            self.can_press_start = True
    
    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        self.start_cooldown()
        # Movement Handling
        prev_direction = self.direction.copy()
        self.direction.y = -1 if keys[pygame.K_UP] or (self.controller_1 and self.controller_1.get_button(self.dpad_up)) else \
                           1 if keys[pygame.K_DOWN] or (self.controller_1 and self.controller_1.get_button(self.dpad_down)) else 0
        
        self.direction.x = -1 if keys[pygame.K_LEFT] or (self.controller_1 and self.controller_1.get_button(self.dpad_left)) else \
                           1 if keys[pygame.K_RIGHT] or (self.controller_1 and self.controller_1.get_button(self.dpad_right)) else 0

        if self.direction != prev_direction:
            print(f"Direction pressed: {self.direction}")

        # Shooting Direction
        self.shoot_direction.y = -1 if keys[pygame.K_w] else 1 if keys[pygame.K_s] else 0
        self.shoot_direction.x = -1 if keys[pygame.K_a] else 1 if keys[pygame.K_d] else 0

        # Menu Navigation
        self.menu_navigation.y = -self.direction.y 
        self.menu_navigation.x = self.direction.x 

        # Menu Selection
        if keys[pygame.K_RETURN] or (self.controller_1 and self.controller_1.get_button(self.x)):
            self.menu_select = 1
            print(f"Menu Select = {self.menu_select}")

        # Escape Key for Menu Toggle

        if (keys[pygame.K_ESCAPE] or (self.controller_1 and self.controller_1.get_button(self.start))) and self.can_press_start:
              # Update the last press time:
            self.can_press_start = False
            self.start_time = pygame.time.get_ticks()
            if not config['menu']['menu_running']:
                config['menu']['menu'].resume_menu()

        # Handle KEYUP Events
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                self.menu_navigation.y = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.menu_navigation.x = 0
            if event.key == pygame.K_RETURN or (self.controller_1 and event.key == self.x):
                self.menu_select = 0
                print(f"Menu Select = {self.menu_select}")