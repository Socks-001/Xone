import pygame

class Controls:
    def __init__(self, menu_running):
        pygame.joystick.init()
        self.controller_found = None
        self.joystick = None
        self.dpad_input_player1 = (0, 0)
        self.button_input_player1 = 0
        #self.button_input_player1 = 0
        self.coolingdown = False
        self.direction = pygame.math.Vector2()
        self.shoot_direction = pygame.math.Vector2()
        self.menu_navigation = pygame.math.Vector2()
        self.menu_running = menu_running
        self.menu_select = 0  # Initialize menu selection state

        # Initialize joysticks
        try:
            self.joystick = pygame.joystick.Joystick(0)  # Initialize the first joystick
            if self.joystick:
                self.controller_found = True
                print("Joystick found")
                self.dpad_up = 11
                self.dpad_down = 12
                self.dpad_left = 13
                self.dpad_right = 14
                self.x = self.joystick.get_button(0)  # Example button, change as needed
                self.square = self.joystick.get_button(2)
                self.triangle = self.joystick.get_button(3)
                self.circle = self.joystick.get_button(1)  
            else:
                print("No joystick found")
        except pygame.error as e:
            print(f"Joystick initialization failed: {e}")

    def handle_event(self, event):
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        if keys[pygame.K_UP] or self.dpad_up:
            self.direction.y = -1
            self.menu_navigation.y = 1
        elif keys[pygame.K_DOWN] or self.dpad_down:
            self.direction.y = 1
            self.menu_navigation.y = -1
        else:
            self.direction.y = 0
            self.menu_navigation.y = 0
        if keys[pygame.K_LEFT] or self.dpad_left:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT] or self.dpad_right:
            self.direction.x = 1
        else:
            self.direction.x = 0
            self.menu_navigation.x = 0
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
            
        elif event.type == pygame.KEYUP:
            if  keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                self.menu_navigation.y = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                self.menu_navigation.x = 0 # Example action for accessing the menu
            if keys[pygame.K_RETURN] or self.x:  # Example action for accessing the menu
                self.menu_select = 0