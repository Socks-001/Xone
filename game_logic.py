import pygame
from utilities import import_csv_layout, import_folder
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILESIZE, BG_COLOR, FPS
from tile import Tile
from player import Player
from menu import Menu
from controls import Controls

def quit(self):
    print("Quitting game...")
    pygame.quit()
    exit()

class Game:
    def __init__(self, screen, scale_factor_list, scale_factor_index, scale_factor):
        # Initializing screen and surface 
        self.screen = screen
        self.scale_factor_list = scale_factor_list
        self.scale_factor_index = scale_factor_index    
        self.scale_factor = scale_factor
        self.game_surface = pygame.Surface((SCREEN_WIDTH *  self.scale_factor , SCREEN_HEIGHT * self.scale_factor))
        self.shared_flags = {'reload_surface': False}
        
        # Initialize Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Initialize player and level
        self.player = None
        self.lvl = 1
        self.running = False
        self.menu_running = True
        
        # Initialize controls
        self.controls = Controls(self.menu_running)
        self.menu = Menu(self.menu_running, self.screen, self.scale_factor_list, self.scale_factor_index, self.scale_factor, self.shared_flags, quit)
    
    
    def create_map(self):
        # Create level counter
        layouts = {
            'floor': import_csv_layout(f'level_data/{self.lvl}/floor.csv'),
            'wall': import_csv_layout(f'level_data/{self.lvl}/wall.csv'),
            'entities': import_csv_layout(f'level_data/{self.lvl}/entities.csv'),
        }
        graphics = {
            'floor': import_folder('graphics/level'),
            'wall': import_folder('graphics/level'),
            'entities': import_folder('graphics/level'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != "-1":
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE

                        if style == 'floor':
                            surf = graphics['floor'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'floor', surf)
                        if style == 'wall':
                            surf = graphics['wall'][int(col)]
                            Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'wall', surf)
                        elif style == 'entities':
                            if col == '19':
                                self.create_player((x, y))
                            else:
                                surf = graphics['entities'][int(col)]
                                Tile((x, y), [self.visible_sprites], 'entities', surf)

    def create_player(self, pos):
        self.player = Player(pos, [self.visible_sprites], self.obstacle_sprites, self.controls, self.menu)
        print(f'Player created at {pos}')

    def run(self):
        print('Starting game...')
        running = True
        self.create_map()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit(self)
                else:
                    self.controls.handle_event(event)
                   
            self.game_surface.fill(BG_COLOR)

            if self.menu.running:
                self.menu.update(self.controls,self.game_surface)

            else:
                self.visible_sprites.draw(self.game_surface)
                self.visible_sprites.update()
            
            if self.shared_flags['reload_surface']:
                self.game_surface = pygame.transform.scale(self.game_surface, (self.screen.get_width(), self.screen.get_height()))
                self.shared_flags['reload_surface']= False
                print(f'shared flags = {self.shared_flags}')

            
            self.screen.blit(self.game_surface, (0, 0))
            pygame.display.flip()
            pygame.event.pump()
