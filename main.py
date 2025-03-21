import pygame, sys
from game_logic import Game
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

class MainLoop:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        self.scale_factor_list = [1, 2, 4, 6]
        self.scale_factor_index = 0
        self.scale_factor = self.scale_factor_list[self.scale_factor_index]
        self.screen = pygame.display.set_mode((SCREEN_WIDTH * self.scale_factor, SCREEN_HEIGHT * self.scale_factor), pygame.RESIZABLE)
        self.FPS = FPS

        # Set Caption
        self.clock = pygame.time.Clock()
        avg_fps = pygame.Clock.get_fps
        pygame.display.set_caption(f'DC{avg_fps}')
        
        
        self.game = Game()
        print("Game initialized.")


    def run(self):
        while True: 
            print("Starting main loop...")
            self.game.run()
            self.clock.tick(FPS)

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()

    #cool