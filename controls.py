import pygame

class Controls:
    def __init__(self):
        self.controller_found = None
        self.joystick = None
        self.dpad_input_player1 = (0, 0)
        self.button_input_player1 = 0
        self.coolingdown = False
        self.direction = pygame.math.Vector2()
        self.shoot_direction = pygame.math.Vector2()

        # Initialize joysticks
        try:
            joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
            if joysticks:
                self.joystick = joysticks[0]
                self.joystick.init()
                self.controller_found = True
                print("Joystick found")
            else:
                print("No joystick found")
        except pygame.error as e:
            print(f"Joystick initialization failed: {e}")

    def input(self):
        keys = pygame.key.get_pressed()

        # Handle keyboard input for movement
        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        # Handle keyboard input for shooting
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

        if keys[pygame.K_ESCAPE]:
            print('Quitting game...')
            pygame.quit()
            exit()

        # Handle controller input if a controller is found
        if self.controller_found:
            try:
                dpad_up = self.joystick.get_button(11)
                dpad_down = self.joystick.get_button(12)
                dpad_left = self.joystick.get_button(13)
                dpad_right = self.joystick.get_button(14)
                self.button_input_player1 = self.joystick.get_button(0)
            except pygame.error as e:
                print(f"Error getting joystick input: {e}")

            if dpad_up:
                print("D-pad up pressed")
                self.direction.y = -1
            elif dpad_down:
                print("D-pad down pressed")
                self.direction.y = 1
            else:
                self.direction.y = 0

            if dpad_left:
                print("D-pad left pressed")
                self.direction.x = -1
            elif dpad_right:
                print("D-pad right pressed")
                self.direction.x = 1
            else:
                self.direction.x = 0