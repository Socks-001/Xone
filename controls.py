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
        
        # D-Pad (digital)
        self.dpad_up = search_dict(config, 'dpad_up')
        self.dpad_down = search_dict(config, 'dpad_down')
        self.dpad_left = search_dict(config, 'dpad_left')
        self.dpad_right = search_dict(config, 'dpad_right')
        
        # face buttons 
        self.x = search_dict(config, 'x')  
        self.square = search_dict(config, 'square')
        self.triangle = search_dict(config, 'triangle')
        self.circle = search_dict(config, 'circle')

        # start / options
        self.start = search_dict(config, 'start')
        self.share = search_dict(config, 'share')
        self.ps = search_dict(config, 'ps')

        # thumb clicks
        self.l_stick_press = search_dict(config, 'l_stick_press')
        self.r_stick_press = search_dict(config, 'r_stick_press')

        # bumpers
        self.l_bumper = search_dict(config, 'l_1')
        self.r_bumper = search_dict(config, 'r_1')

        # touchpad
        self.touchpad = search_dict(config, 'touchpad')

        # analog axes
        self.l_stick_x = search_dict(config, 'left_stick_x')
        self.l_stick_y = search_dict(config, 'left_stick_y')
        self.r_stick_x = search_dict(config, 'right_stick_x')
        self.r_stick_y = search_dict(config, 'right_stick_y')
        self.r2_axis = search_dict(config, 'r2_axis')
        self.l2_axis = search_dict(config, 'l2_axis')

        

    def get_action_map(self):
        MENU_INPUT_THRESHOLD = 0.5
        if self.menu_navigation != (0, 0):
            pass
            #print(f'Menu nav = {self.menu_navigation}')
        return {
            'menu_up': self.menu_navigation.y < -MENU_INPUT_THRESHOLD,
            'menu_down': self.menu_navigation.y > MENU_INPUT_THRESHOLD,
            'menu_select': self.menu_select == 1,
            # Add other mappings as needed (like 'pause', etc.)
        }
    
    def start_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_press_start:
            if (current_time - self.start_time) >= self.button_cooldown:
                print(f"Cooldown finished, allowing press again at {current_time}")
                self.can_press_start = True
    
    def handle_event(self, event):
        keys = pygame.key.get_pressed()
        # set right stick and left stick input 

        right_stick_x = self.controller_1.get_axis(self.r_stick_x)  # Right stick X-axis
        right_stick_y = self.controller_1.get_axis(self.r_stick_y)  # Right stick Y-axis
        left_stick_x = self.controller_1.get_axis(self.l_stick_x)  # Left stick X-axis (for movement, if needed)
        left_stick_y = self.controller_1.get_axis(self.l_stick_y)  # Left stick Y-axis (for movement, if needed)
        rightstick_input = pygame.Vector2(right_stick_x, right_stick_y)
        leftstick_input = pygame.Vector2(left_stick_x, left_stick_y)

        self.start_cooldown()
        # Movement Handling
        if abs(left_stick_x) < 0.10 or abs(left_stick_x) > 1 :
            left_stick_x = 0
        if abs(left_stick_y) < 0.10 or abs(left_stick_y) > 1 :
            left_stick_y = 0
        if leftstick_input.length() > 0.10:
            self.direction = leftstick_input
        
            print (f"Left Stick Input: {leftstick_input.length}")
        
        else:
            # Fallback to WASD
            kb_x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            kb_y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
            self.direction = pygame.Vector2(kb_x, kb_y)

                # Deadzone check
        if abs(right_stick_x) < 0.10 or abs(right_stick_x) > 1 :
            right_stick_x = 0
        if abs(right_stick_y) < 0.10 or abs(right_stick_y) > 1 :
            right_stick_y = 0
        if rightstick_input.length_squared() > 0.10:
            self.shoot_direction = rightstick_input
        else:
            # Fallback to WASD
            kb_s_x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
            kb_s_y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
            self.shoot_direction = pygame.Vector2(kb_s_x, kb_s_y)

        # Optional: Normalize for consistent direction regardless of stick strength
        if self.shoot_direction.length_squared() > 0:
            self.shoot_direction = self.shoot_direction.normalize()

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
            print(f"Start/ESC button pressed at {self.start_time}")
            if config['menu']['menu_running'] is False:
                config['menu']['menu'].resume_menu()
            elif config['menu']['menu_running'] is True:
                config['menu']['menu'].resume_game()
            print(f"Menu Running = {config['menu']['menu_running']}")

        # Handle KEYUP Events
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                self.menu_navigation.y = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.menu_navigation.x = 0
            if event.key == pygame.K_RETURN or (self.controller_1 and event.key == self.x):
                self.menu_select = 0  
                #print(f"Menu Select = {self.menu_select}")