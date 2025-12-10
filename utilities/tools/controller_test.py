#controller test 
import pygame
import sys

def initialize_pygame():
    pygame.init()

def main():
    initialize_pygame()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption('Joystick Test')

    # Initialize joysticks
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    for joystick in joysticks:
        joystick.init()
        print(f"Joystick {joystick.get_instance_id()} - {joystick.get_name()} initialized")
        print(f"Number of axes: {joystick.get_numaxes()}")
        print(f"Number of buttons: {joystick.get_numbuttons()}")
        print(f"Number of hats: {joystick.get_numhats()}")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.JOYAXISMOTION:
                if event.value > 0.02: # Deadzone threshold
                    print(f"Joystick {event.joy} axis {event.axis} motion: {event.value}")
            elif event.type == pygame.JOYBUTTONDOWN:
                print(f"Joystick {event.joy} button {event.button} down")
            elif event.type == pygame.JOYBUTTONUP:
                print(f"Joystick {event.joy} button {event.button} up")
            elif event.type == pygame.JOYHATMOTION:
                print(f"Joystick {event.joy} hat {event.hat} motion: {event.value}")
        
        #print(f'pygame axis 3: {joysticks[0].get_axis(3)}, pygame axis 2: {joysticks[0].get_axis(2)}')

        screen.fill((0, 0, 0))
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()