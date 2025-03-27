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
        self.scale_factor_index = 0
        self.scale_factor_list = [1, 2, 4, 6]
        self.scale_factor = self.scale_factor_list[self.scale_factor_index] 
        print (f'scale factor index = {self.scale_factor_index}, scale factor = {self.scale_factor}')
        self.screen_width = search_dict(config,'SCREEN_WIDTH')
        self.screen_height = search_dict(config,'SCREEN_HEIGHT')
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_surface = pygame.Surface((self.screen_width, self.screen_height))
        
        # Update settings dictionary
        config['screen']['screen'] = self.screen 
        config['screen']['game_surface'] = self.game_surface
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = search_dict(config, 'FPS')
        pygame.display.set_caption('DC')
        
        # Game
        self.controls = Controls()
        self.game = Game(self.controls)
        print("Game initialized.")
        config['lvl']['game'] = self.game
        
        

        # Menu
        self.menu = Menu()
        config['menu']['menu'] = self.menu
    
    '''def handle_scaling(self):
        if config['screen']['scale_surface_trigger']:
            print('Scaling...')
            self.scale_factor_index = (self.scale_factor_index + 1) % len(self.scale_factor_list)
            self.scale_factor = self.scale_factor_list[self.scale_factor_index]  # Update scale_factor based on the index
            print(f'scale factor index = {self.scale_factor_index}, scale factor = {self.scale_factor}')
            self.screen = pygame.display.set_mode(((self.screen_width * self.scale_factor), (self.screen_height * self.scale_factor)), pygame.SCALED)
            scaled_surface = pygame.transform.scale(self.game_surface, self.screen.get_size())
            config['screen']['game_surface'] = scaled_surface
            config['screen']['scale_surface_trigger'] = False'''
            

    def handle_fullscreen(self):
        if config['screen']['fullscreen_trigger']:
            display_info = pygame.display.Info()
            display_width = display_info.current_w
            display_height = display_info.current_h
                
            if pygame.display.get_surface().get_flags() & pygame.FULLSCREEN:
                # If the game is in fullscreen mode, toggle back to windowed mode
                print("Exiting fullscreen...")
                self.screen = pygame.display.set_mode((self.screen_width * self.scale_factor, self.screen_height * self.scale_factor), pygame.SCALED)
                self.game_surface = pygame.Surface((self.screen_width, self.screen_height))  # Reset the game surface to original size
            else:
                # Set the game window to fullscreen
                print("Entering fullscreen...")
                self.screen = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN | pygame.SCALED)
                scaled_surface = pygame.transform.scale(self.game_surface, (display_width, display_height))
                config['screen']['game_surface'] = scaled_surface
                self.game_surface = config['screen']['game_surface']
        
        config['screen']['fullscreen_trigger'] = False

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

                # Handle scaling and fullscreen changes
                #self.handle_scaling()
                self.handle_fullscreen()

                self.screen.blit(self.game_surface, (0, 0))
                pygame.display.flip()
                pygame.event.pump()
                self.clock.tick(self.fps)
                pygame.display.set_caption(f'DC {self.clock.get_fps():.2f}')

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()