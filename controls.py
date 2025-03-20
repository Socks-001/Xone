import pygame

class Controls:
    def __init__(self, game):
        self.controller_found = None
        self.joystick = None
        self.dpad_input_player1 = (0, 0)
        self.button_input_player1 = 0
        self.coolingdown = False
        self.direction = pygame.math.Vector2()
        self.shoot_direction = pygame.math.Vector2()
        self.menu_navigation = pygame.math.Vector2()
        self.game = game

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

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.direction.y = -1
                self.menu_navigation.y = 1
            elif event.key == pygame.K_DOWN:
                self.direction.y = 1
                self.menu_navigation.y = -1
            else:
                self.direction.y = 0
            if event.key == pygame.K_LEFT:
                self.direction.x = -1
            elif event.key == pygame.K_RIGHT:
                self.direction.x = 1
            else:
                self.direction.x = 0
            if event.key == pygame.K_w:
                self.shoot_direction.y = -1
            elif event.key == pygame.K_s:
                self.shoot_direction.y = 1
            else:
                self.shoot_direction.y = 0
            if event.key == pygame.K_a:
                self.shoot_direction.x = -1
            elif event.key == pygame.K_d:
                self.shoot_direction.x = 1
            else:
                self.shoot_direction.x = 0
            if event.key == pygame.K_ESCAPE:
                self.game.menu_running = not self.game.menu_running  # Example action for accessing the menu

        
