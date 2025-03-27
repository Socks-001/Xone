import pygame
from utilities import search_dict
from settings import config, add_joystick_buttons

class Controls:
    def __init__(self):
        pygame.joystick.init()
        self.joystick_1 = None
        self.dpad_input_player1 = (0, 0)
        self.button_input_player1 = 0
        self.coolingdown = False
        self.direction = pygame.math.Vector2()
        self.shoot_direction = pygame.math.Vector2()
        self.menu_navigation = pygame.math.Vector2()
        self.menu_select = 0  # Initialize menu selection state

        # Initialize joysticks
        try:
            joystick_count = pygame.joystick.get_count()

            if joystick_count > 0:
                self.controller_found = True
                for i in range(joystick_count):
                    joystick = pygame.joystick.Joystick(i)
                    joystick.init()
                    print(f"Joystick {i} found: {joystick.get_name()}")
                else:
                    print("No joystick found")
                if pygame.joystick.Joystick(0):
                    self.joystick_1 = pygame.joystick.Joystick(0)
                    add_joystick_buttons(self.joystick_1)
                    print("Joystick found")
                    self.dpad_up = search_dict(config,'dpad_up')
                    self.dpad_down = search_dict(config,'dpad_down')
                    self.dpad_left = search_dict(config,'dpad_left')
                    self.dpad_right = search_dict(config,'dpad_right')
                    self.x = search_dict(config,'x')  
                    self.square = search_dict(config,'square')
                    self.triangle = search_dict(config,'triangle')
                    self.circle = search_dict(config,'circle')
        except pygame.error as e:
            print(f"Joystick initialization failed: {e}")

    def handle_event(self, event):
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        if keys[pygame.K_UP] or self.dpad_up:
            self.direction.y = -1
            self.menu_navigation_y = 1
            print(f'up , {self.direction.y}')
        elif keys[pygame.K_DOWN] or self.dpad_down:
            self.direction.y = 1
            self.menu_navigation_y = -1
            print(f'down , {self.direction.y}')
        else:
            self.direction.y = 0
            self.menu_navigation_y = 0
        if keys[pygame.K_LEFT] or self.dpad_left:
            self.direction.x = -1
            self.menu_navigation_x = 1
            print(f'left , {self.direction.x}')
        elif keys[pygame.K_RIGHT] or self.dpad_right:
            self.direction.x = 1
            self.menu_navigation_x = -1
            print(f'right , {self.direction.x}')
        else:
            self.direction.x = 0
            self.menu_navigation_x = 0
        if keys[pygame.K_w]:
            self.shoot_direction.y = -1
        elif keys[pygame.K_s]:
            self.shoot_direction.y = 1
        else:
            self.shoot_direction.y = 0
        if keys[pygame.K_a]:
            self.shoot_direction.x = -1
        elif keys[pygame.K_d]:
            self.shoot_direction.x = 1
        else:
            self.shoot_direction.x = 0
        if keys[pygame.K_RETURN] or self.x:  # Example action for accessing the menu
            self.menu_select = 1
            print (f'menu_select = {self.menu_select}')
        if keys[pygame.K_ESCAPE]:
            if not config['menu']['menu_running']:
                config['menu']['menu_running'] = True
            
        elif event.type == pygame.KEYUP:
            if  keys[pygame.K_UP] or keys[pygame.K_DOWN] or not self.dpad_up or not self.dpad_down:
                self.menu_navigation_y = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or not self.dpad_left or not self.dpad_right:
                self.menu_navigation_x = 0 # Example action for accessing the menu
            if keys[pygame.K_RETURN] or self.x:  # Example action for accessing the menu
                self.menu_select = 0
                print (f'menu_select = {self.menu_select}')
