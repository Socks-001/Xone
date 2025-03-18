import pygame
from utilities import import_csv_layout, import_folder
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, TILESIZE, BG_COLOR, FPS
from tile import Tile
from player import Player
from menu import Menu

class Game:
    def __init__(self):

        # Create a smaller surface for the original resolution
        self.game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # General Setup
        self.clock = pygame.time.Clock()
        self.scale_factor_list = [1,2,4,6]
        self.scale_factor_index = 0
        self.scale_factor = self.scale_factor_list[self.scale_factor_index]
        self.screen = pygame.display.set_mode((SCREEN_WIDTH * self.scale_factor, SCREEN_HEIGHT * self.scale_factor))

        #Initialize Sprite Groups
        self.visible_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()

        # Initialize player and level
        self.player = None
        
        #initialize player
        self.lvl = 1
        self.running = False
        self.cycle = 0
        self.time = 0
        self.menu = Menu()
        
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
        self.player = Player(pos, [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        print ('Starting game...')
        running = True
        while running : 
            if self.menu.running:
                self.menu.update()
                self.menu.draw(self.game_surface)
            else:
                self.game_surface.fill(BG_COLOR)
                self.visible_sprites.update()
                self.visible_sprites.draw(self.game_surface)
            
            self.screen.blit(self.game_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.event.pump()