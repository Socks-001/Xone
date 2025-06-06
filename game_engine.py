import pygame
from map_generation import Game
from menu import Menu
from config import config
from level_data import level
from controls import Controls
from debug import sprite_group_highlight
from utilities import draw_point, get_surface_center

class GameEngine:
    def __init__(self, screen, game_surface):
        # Screen and Surface
        self.screen = screen
        self.game_surface = game_surface
        self.screen_center = get_surface_center(self.screen)
        self.game_surface_center = get_surface_center(self.game_surface)
        self.game_surface_centering_coordinates = ((self.screen_center[0] - self.game_surface_center[0]), (self.screen_center[1] - self.game_surface_center[1]))

        # Clock
        self.clock = pygame.time.Clock()
        self.fps = config['screen']['FPS']
        pygame.display.set_caption('DC')

        # Game
        self.controls = Controls()
        self.game = Game(self.controls)
        level['level_config']['game'] = self.game

        # Sprite Groups
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.weapon_sprites = level['sprite_groups']['weapons_sprites']

        # Menu
        self.menu = Menu()
        config['menu']['menu'] = self.menu

    def handle_fullscreen(self):
        if config['screen']['fullscreen_trigger']:
            pygame.display.toggle_fullscreen()
            config['screen']['fullscreen_trigger'] = False
    
    def get_sprite_groups_from_dict(self):
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.weapon_sprites = level['sprite_groups']['weapons_sprites']
        self.player_sprites = level['sprite_groups']['player_sprites']
        self.enemy_sprites = level['sprite_groups']['enemy_sprites']
        self.floor_sprites = level['sprite_groups']['floor_sprites']
        self.wall_sprites = level['sprite_groups']['wall_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        self.light_sprites = level['sprite_groups']['light_sprites']
    
    def update_sprite_groups(self):
        self.weapon_sprites.update()
        self.entity_sprites.update()
        self.floor_sprites.update()
        self.wall_sprites.update()
        self.light_sprites.update()
        
    def draw_game_scene(self, debug):
        self.game_surface.fill(config['ui']['colors']['BG_COLOR'])
        self.get_sprite_groups_from_dict()
        self.update_sprite_groups()
        self.debug_bool = config['debug']['projectile_lines']
        
        self.floor_sprites.draw(self.game_surface) 
        self.wall_sprites.draw(self.game_surface)
        for weapon in self.weapon_sprites:
            weapon.draw(self.game_surface, self.debug_bool)
        self.entity_sprites.draw(self.game_surface)
        self.light_sprites.draw(self.game_surface)


        if debug == True:
             # Highlight walls
            if config['debug']['walls_debug']:
                sprite_group_highlight(self.wall_sprites, self.game_surface, 1, 1)

            # Highlight players
            if config['debug']['player_debug']:
                sprite_group_highlight(self.player_sprites, self.game_surface, 2, 1)

            # Highlight enemies
            if config['debug']['enemies_debug']:
                sprite_group_highlight(self.enemy_sprites, self.game_surface, 3, 1)

            # Highlight weapons
            if config['debug']['weapons_debug']:
                sprite_group_highlight(self.weapon_sprites, self.game_surface, 4, 1)
            

    def run(self):
        while True:
            level['level_config']['game_running'] = True
            self.game_running = level['level_config']['game_running']

            while self.game_running:
                self.controls.update()
                self.game_surface.fill(config['ui']['colors']['BG_COLOR'])
                action_map = self.controls.get_action_map()
                if config['menu']['menu_running']:
                    self.menu.update(action_map, self.game_surface)
                else:
                   self.draw_game_scene( debug=config['debug']['debug'])

                # Handle scaling and fullscreen changes
                self.handle_fullscreen()
                
                self.screen.blit(self.game_surface, self.game_surface_centering_coordinates)
                draw_point(self.screen, color = (200,255,200, 255))

                pygame.display.flip()
                pygame.event.pump()
                self.clock.tick(self.fps)
                pygame.display.set_caption(f'DC {self.clock.get_fps():.2f}')