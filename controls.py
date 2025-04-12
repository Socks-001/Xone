import pygame
from utilities import search_dict
from config import config, add_joystick_buttons

class Controls:
    def __init__(self):
        pygame.joystick.init()
        self.controller_1 = None
        self.has_controller = None
        self.dpad_input_player1 = (0, 0)
        self.button_input_player1 = 0
        self.direction = pygame.math.Vector2()
        self.shoot_direction = pygame.math.Vector2()
        self.menu_navigation = pygame.math.Vector2()
        self.menu_select = False  # Initialize menu selection state

        # Cooldown for the start button
        self.button_cooldown = 500  # Cooldown in milliseconds (e.g., 500ms)
        self.can_press_start = True  # Last time the start button was pressed
        self.start_time = 0  # Initialize the last press time
        self.start_pressed = False
        #self.prev_start_button = False

        # Initialize joysticks
        try:
            if pygame.joystick.get_count() > 0:
                self.controller_1 = pygame.joystick.Joystick(0)
                self.controller_1.init()
                print(f"Joystick found: {self.controller_1.get_name()}")
                add_joystick_buttons(self.controller_1)
                self._load_joystick_config()
                self.has_controller = True
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
            'menu_select': self.menu_select,
            'paused': self.start_pressed,
            # Add other mappings as needed (like 'pause', etc.)
        }
    
    def start_cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_press_start:
            if (current_time - self.start_time) >= self.button_cooldown:
                print(f"Cooldown finished, allowing press again at {current_time}")
                self.can_press_start = True

    def apply_deadzone(self, value, threshold=0.10, upper_limit=1.0):
        return 0 if abs(value) < threshold or abs(value) > upper_limit else value

    def process_input_event(self, event):
        right_stick_x = 0
        right_stick_y = 0
        left_stick_x = 0
        left_stick_y = 0
        
        keys = pygame.key.get_pressed()
        
        # set right stick and left stick input 
        if self.has_controller : 
            right_stick_x = self.apply_deadzone(self.controller_1.get_axis(self.r_stick_x))  # Right stick X-axis
            right_stick_y = self.apply_deadzone(self.controller_1.get_axis(self.r_stick_y))  # Right stick Y-axis
            left_stick_x = self.apply_deadzone(self.controller_1.get_axis(self.l_stick_x))  # Left stick X-axis (for movement, if needed)
            left_stick_y = self.apply_deadzone(self.controller_1.get_axis(self.l_stick_y))  # Left stick Y-axis (for movement, if needed)
            rightstick_input = pygame.Vector2(right_stick_x, right_stick_y)
            leftstick_input = pygame.Vector2(left_stick_x, left_stick_y)

        self.start_cooldown()

        # Movement Handling
        if leftstick_input.length() > 0.10:
            self.direction = leftstick_input.normalize()
            # print (f"Left Stick Input: {leftstick_input.length}")
        
        else:
            # Fallback to WASD
            kb_x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
            kb_y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
            self.direction = pygame.Vector2(kb_x, kb_y)

        # Set Shooting Direction 
        if rightstick_input.length_squared() > 0.10:
            self.shoot_direction = rightstick_input.normalize()

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

        if self.has_controller:
            # Detect Button Down
            if event.type == pygame.JOYBUTTONDOWN :
                if event.button == self.x : 
                    self.menu_select = True
                if event.button == self.start and self.can_press_start:
                    self.start_pressed = True
                    self.can_press_start = False
                    self.start_time = pygame.time.get_ticks()
            # Detect jostick up
            elif event.type == pygame.JOYBUTTONUP : 
                if event.button == self.x : 
                    self.menu_select = False
                if event.button == self.start : 
                    self.start_pressed = False

         # Detect KEYDOWN Events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.menu_select = True
            if event.key == pygame.K_ESCAPE:
                self.start_pressed = True

        # Detect KEYUP Events
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                self.menu_navigation.y = 0
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                self.menu_navigation.x = 0
            if event.key == pygame.K_RETURN:
                self.menu_select = False
            if event.key == pygame.K_ESCAPE:
                self.start_pressed = False
    
    def toggle_menu(self):
        self.start_pressed = False
        if config['menu']['menu_running'] is False:
            config['menu']['menu'].resume_menu()
        elif config['menu']['menu_running'] is True:
            config['menu']['menu'].resume_game()
        print(f"Menu Running = {config['menu']['menu_running']}")
        
        

    def update(self):
        action_map = self.get_action_map()
        # Get current button state for Start

        if action_map.get('paused'):
            self.toggle_menu()
    
        self.start_cooldown()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else: 
                self.process_input_event(event)