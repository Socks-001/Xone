import pygame, sys
from game_logic import Game
from settings import config
from utilities import search_dict


class MainLoop:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        scale_factor = search_dict(config,'SCALE_FACTOR_LIST')[search_dict(config,'SCALE_FACTOR_INDEX')]
        screen = pygame.display.set_mode((search_dict(config,'SCREEN_WIDTH') * scale_factor, search_dict(config,'SCREEN_HEIGHT') * scale_factor), pygame.RESIZABLE)
        self.screen = search_dict(config,'SCREEN') 
        self.fps = search_dict(config,'FPS')
        

        # Set Caption
        self.clock = pygame.time.Clock()
        AVG_FPS = pygame.Clock.get_fps
        pygame.display.set_caption(f'DC{AVG_FPS}')
        
        self.game = Game()
        print("Game initialized.")

    def run(self):
        while True: 
            print("Starting main loop...")
            self.game.run()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()

    #cool