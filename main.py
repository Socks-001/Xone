import pygame
from sys import exit
from game_logic import Game
from menu import Menu
from settings import config
from level_data import level, load_level_data
from utilities import search_dict
from controls import Controls
from debug import sprite_group_highlight

class MainLoop:
    def __init__(self):
        print("Initializing Pygame...")
        pygame.init()
        
        # Display 
        self.bg_color = search_dict(config,'BG_COLOR')
        self.scale_factor = 4
        self.screen_width = search_dict(config,'SCREEN_WIDTH')
        self.screen_height = search_dict(config,'SCREEN_HEIGHT')
        self.screen = pygame.display.set_mode((self.screen_width * self.scale_factor, self.screen_height * self.scale_factor), pygame.SCALED)
        
        # Update Dictionary 
        config['screen']['screen'] = self.screen 
        config['screen']['game_surface'] = self.game_surface = pygame.Surface((self.screen_width, self.screen_height))
        config['screen']['scaled_surface'] = self.scaled_surface = pygame.transform.scale(self.game_surface, (self.screen_width, self.screen_height))
        
        # Clock
        self.clock = pygame.time.Clock()
        self.fps = search_dict(config, 'FPS')
        pygame.display.set_caption('DC')
        
        # Game
        self.controls = Controls()
        self.game = Game(self.controls)
        print("Game initialized.")
        level['level_config']['game'] = self.game
        
        # Sprite Groups
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']

        # Menu
        self.menu = Menu()
        config['menu']['menu'] = self.menu
            
    def handle_fullscreen(self):
        if config['screen']['fullscreen_trigger'] :
            pygame.display.toggle_fullscreen()
            config['screen']['fullscreen_trigger'] = False

    def run(self):
        while True: 
            print("Starting main loop...")
            level['level_config']['game_running'] = True
            self.game_running = level['level_config']['game_running']
            
            
            while self.game_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        level['level_config']['game_running'] = False
                        pygame.quit()
                        exit()
                    else:
                        self.controls.handle_event(event)
                       
                self.game_surface.fill(self.bg_color)

                if config['menu']['menu_running']:
                    self.menu.update(self.controls, self.game_surface)
                else:
                    self.visible_sprites = level['sprite_groups']['visible_sprites']
                    self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
                    self.visible_sprites.draw(self.game_surface)
                    self.visible_sprites.update()

                # Handle scaling and fullscreen changes
                #self.handle_scaling()
                self.handle_fullscreen()
                self.scaled_surface = pygame.transform.scale(self.game_surface, self.screen.get_size())
                config['screen']['scaled_surface'] = self.scaled_surface
                self.screen.blit(self.scaled_surface, (0, 0))
                
                sprite_group_highlight(self.obstacle_sprites)

                pygame.display.flip()
                pygame.event.pump()
                self.clock.tick(self.fps)
                pygame.display.set_caption(f'DC {self.clock.get_fps():.2f}')

if __name__ == '__main__':
    main_game = MainLoop()
    main_game.run()