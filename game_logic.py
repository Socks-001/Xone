import pygame
from utilities import import_csv_layout, import_folder, search_dict
from settings import config
from tile import Tile
from player import Player
from menu import Menu
from controls import Controls



class Game:
    def __init__(self):
        # Initializing screen and surface 
        self.screen = search_dict(config,'screen')
        self.game_surface = search_dict(config,'game_surface')
        self.bg_color = search_dict(config,'BG_COLOR')
        self.tilesize = search_dict(config,'TILESIZE')
        
        # Initialize Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Initialize player and level
        self.player = None
        self.lvl = search_dict(config,'lvl_number')
        self.game_running = search_dict(config,'game_running')
        self.menu_running = search_dict(config,'menu_running')


        # Initialize controls
        self.controls = Controls()
        self.menu = Menu()

        self.create_map()
    
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
                        x = col_index * self.tilesize
                        y = row_index * self.tilesize

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
        self.player = Player(pos, [self.visible_sprites], self.obstacle_sprites, self.controls, self.menu_running)
        print(f'Player created at {pos}')

    def run(self):
        print('Starting game...')
        
        while self.game_running['game_running']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                    quit(self)
                else:
                    self.controls.handle_event(event)
                   
            self.game_surface.fill(self.bg_color)

            if self.menu_running:
                self.menu.update(self.controls,self.game_surface)

            else:
                self.visible_sprites.draw(self.game_surface)
                self.visible_sprites.update()
            
            self.screen.blit(self.game_surface, (0, 0))
            pygame.display.flip()
            pygame.event.pump()
