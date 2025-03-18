import pygame
from game_logic import Game

class MainLoop:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        avg_fps=pygame.time.Clock.get_fps
        pygame.display.set_caption(f'DC{avg_fps}')
        self.game = Game()
        print("Game initialized.")
        self.game.create_map()

    def run(self):
        print("Starting main loop...")
        self.game.run()

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()