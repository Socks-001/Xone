import pygame, sys
from game_logic import Game
from menu import Menu
from settings import config
from utilities import search_dict
from controls import Controls

class MainLoop:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        
        # Display 
        self.bg_color = search_dict(config,'BG_COLOR')
        self.scale_factor_index = config['screen']['scale_factor_index']
        self.scale_factor_list = config['screen']['SCALE_FACTOR_LIST']
        self.scale_factor = self.scale_factor_list[self.scale_factor_index] 
        config['menu']['scale_factor'] = self.scale_factor
        print (f'scale_factor = {self.scale_factor}')
        self.screen_width = search_dict(config,'SCREEN_WIDTH')
        self.screen_height = search_dict(config,'SCREEN_HEIGHT')
        self.screen = pygame.display.set_mode((self.screen_width * self.scale_factor, self.screen_height * self.scale_factor), pygame.RESIZABLE)
        self.game_surface = pygame.Surface((self.screen_width, self.screen_height))
        self.fullscreen_trigger = config['screen']['fullscreen_trigger']
        
        # Update settings dictionary
        config['screen']['screen'] = self.screen 
        config['screen']['game_surface'] = self.game_surface
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = search_dict(config, 'FPS')
        pygame.display.set_caption('DC')
        
        # Game
        self.game = Game()
        print("Game initialized.")
        config['lvl']['game'] = self.game
        self.controls = Controls()
        config['controls']['controls'] = self.controls

        # Menu
        self.menu = Menu()
        config['menu']['menu'] = self.menu

    def run(self):
        while True: 
            print("Starting main loop...")
            config['lvl']['game_running'] = True
            self.game_running = config['lvl']['game_running']
            while self.game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        config['lvl']['game_running'] = False
                        pygame.quit()
                        sys.exit()
                    else:
                        self.controls.handle_event(event)
                       
                self.game_surface.fill(self.bg_color)

                if config['menu']['menu_running']:
                    self.menu.update(self.controls, self.game_surface)
                else:
                    self.visible_sprites = config['lvl']['visible_sprites']
                    self.obstacle_sprites = config['lvl']['obstacle_sprites']
                    self.game.visible_sprites.draw(self.game_surface)
                    self.game.visible_sprites.update()
                
                if config['screen']['scale_surface_trigger']:
                    print('scaling')
                    config['screen']['scale_factor'] = (self.scale_factor + 1) % len(self.scale_factor_list)
                    self.scale_factor = config['screen']['scale_factor']
                    self.screen = pygame.display.set_mode((self.screen_width * self.scale_factor, self.screen_height * self.scale_factor), pygame.RESIZABLE)
                    scaled_surface = pygame.transform.scale(self.game_surface, self.screen.get_size())
                    # Update the reference in config
                    config['screen']['game_surface'] = scaled_surface
                    self.game_surface = config['screen']['game_surface']
                    config['screen']['scale_surface_trigger'] = False   
                    
                if config['screen']['fullscreen_trigger']:
                    if self.screen.get_flags() & pygame.FULLSCREEN:
                        config['screen']['screen'] = pygame.display.set_mode(self.screen_width, self.screen_height)
                    else:
                        config['screen']['screen'] = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
                    config['screen']['fullscreen_trigger'] = False

                self.screen.blit(self.game_surface, (0, 0))
                pygame.display.flip()
                pygame.event.pump()
                self.clock.tick(self.fps)
                pygame.display.set_caption(f'DC {self.clock.get_fps():.2f}')

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()