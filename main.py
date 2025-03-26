import pygame, sys
from game_logic import Game
from menu import Menu
from settings import config
from utilities import search_dict


class MainLoop:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        
        # Display 
        self.scale_surface = search_dict(config,'scale_surface')
        self.scale_factor_index = search_dict (config,'scale_factor_index')
        self.scale_factor_list = search_dict (config,'SCALE_FACTOR_LIST')
        self.scale_factor = self.scale_factor_list[self.scale_factor_index] 
        self.screen = pygame.display.set_mode((search_dict(config,'SCREEN_WIDTH') * self.scale_factor, search_dict(config,'SCREEN_HEIGHT') * self.scale_factor), pygame.RESIZABLE)
        self.game_surface = pygame.Surface((config['screen']['SCREEN_WIDTH'] * self.scale_factor, config['screen']['SCREEN_HEIGHT'] * self.scale_factor))
        
        # Update settings dictionary
        config['screen']['screen'] = self.screen 
        config['screen']['game_surface'] = self.game_surface
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = search_dict(config,'FPS')
        pygame.display.set_caption('DC')
        
        # Game
        self.game = Game()
        print("Game initialized.")
        self.game.create_map()
       
        # Menu
        self.menu = Menu()
        self.menu_running = search_dict(config,'menu_running')

    def run(self):
        
        while True: 
            print("Starting main loop...")
            self.game.game_running = True
            while self.game.game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game.game_running = False
                        pygame.quit()
                        sys.exit()
                    else:
                        self.game.controls.handle_event(event)
                       
                #self.game.game_surface.fill(self.game.bg_color)

                if self.menu_running:
                    self.menu.update(self.game.controls, self.game.game_surface)
                else:
                    self.game.visible_sprites.draw(self.game.game_surface)
                    self.game.visible_sprites.update()
                
                if self.scale_surface :
                    self.scale_factor_index = (self.scale_factor_index + 1) % len(self.scale_factor_list)
                    scaled_surface = pygame.transform.scale(self.game_surface, self.screen.get_size())

                    # Update the reference in config
                    config[search_dict(config,'game_surface')] = scaled_surface
                
                self.screen.blit(self.game.game_surface, (0, 0))
                pygame.display.flip()
                pygame.event.pump()
                self.clock.tick(self.fps)
                pygame.display.set_caption(f'DC {self.clock.get_fps():.2f}')

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()