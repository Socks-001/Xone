import pygame
from level_instancer import Game
from menu import Menu
from config import config
from level_data import level
from controls import Controls
from debug import sprite_group_highlight
from utilities import draw_point, get_surface_center
from render_engine_ex import RenderEngineEx


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
        '''self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.wall_sprites = level['sprite_groups']['wall_sprites']
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.weapon_sprites = level['sprite_groups']['weapons_sprites']'''

        # Menu
        self.menu = Menu()
        config['menu']['menu'] = self.menu

        #Rendering
        
        self.render_engine = RenderEngineEx(self.game_surface, self.game_surface_center, None, None)
        self.world_ready = False
        

    def handle_fullscreen(self):
        if config['screen']['fullscreen_trigger']:
            pygame.display.toggle_fullscreen()
            config['screen']['fullscreen_trigger'] = False

    # --- tiny helper in GameEngine ---
    def ensure_stacker_player(self):
        # Try to bind once the menu has built the world
        if not self.world_ready:
            from player_data import player_data
            p = player_data.get("player") or (next(iter(self.player_sprites), None) if len(self.player_sprites) else None)
            if p:
                self.render_engine.player = p
                self.world_ready = True
        else:
            # Re-bind if the player object was replaced (new instance)
            from player_data import player_data
            p = player_data.get("player")
            if p and p is not self.render_engine.player:
                self.render_engine.player = p

    def get_sprite_groups_from_dict(self):
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.weapon_sprites = level['sprite_groups']['weapons_sprites']
        self.player_sprites = level['sprite_groups']['player_sprites']
        self.enemy_sprites = level['sprite_groups']['enemy_sprites']
        self.decor_sprites = level['sprite_groups']['decor_sprites']
        self.floor_sprites = level['sprite_groups']['floor_sprites']
        self.wall_sprites = level['sprite_groups']['wall_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        self.light_sprites = level['sprite_groups']['light_sprites']
    
    def update_sprite_groups(self):
        self.weapon_sprites.update()
        self.entity_sprites.update()
        self.floor_sprites.update()
        self.obstacle_sprites.update()
        self.decor_sprites.update()
        self.light_sprites.update()

    def draw_text(self, screen, text, pos, small=False, align = 'center'):
        
        self.font = pygame.font.SysFont("atkinsonhyperlegiblemonoextralight", 18)
        self.font_small = pygame.font.SysFont("atkinsonhyperlegiblemonoextralight", 8)
        font = self.font_small if small else self.font
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()

        if align == 'center':
            text_rect.center = pos
        elif align == 'right':
            text_rect.midright = pos
        elif align == 'left':
            text_rect.midleft = pos

        screen.blit(text_surface, text_rect)

    def draw_game_scene(self, debug):
        # --- in draw_game_scene() at the very top ---
        self.get_sprite_groups_from_dict()
        self.ensure_stacker_player()
        

        if not self.world_ready:
            return  # no player yet; skip this frame cleanly
        
        
        # world origin dot (magenta)
        
        self.game_surface.fill(config['ui']['colors']['BG_COLOR'])
        self.get_sprite_groups_from_dict()
        self.update_sprite_groups()
        self.debug_bool = config['debug']['projectile_lines']
        self.render_engine.get_current_offset()

        pc = pygame.Vector2(self.render_engine.player.hitbox.center)

        world = pygame.sprite.Group()
        for g in (self.player_sprites, self.enemy_sprites, self.weapon_sprites,
          self.light_sprites, self.wall_sprites, self.decor_sprites):
            world.add(g.sprites())
        
            self.render_engine.visible(self.floor_sprites)
            self.render_engine.visible((world))
        

        self.debug_world_dot(pc, (0,255,0))
        self.debug_world_dot(self.render_engine.world_space_origin, (255,0,255))        

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
            
    def debug_world_dot(self, world_pos, color=(255,0,0)):
        sp = self.render_engine.world_to_screen(world_pos)
        pygame.draw.circle(self.game_surface, color, (int(sp.x), int(sp.y)), 1)

    def run(self):
        while True:
            level['level_config']['game_running'] = True
            self.game_running = level['level_config']['game_running']

            while self.game_running:
                self.controls.update()
                action_map = self.controls.get_action_map()
                if config['menu']['menu_running']:
                    self.menu.update(action_map, self.game_surface)
                else:
                   self.draw_game_scene( debug=config['debug']['debug'])

                # Handle scaling and fullscreen changes
                self.handle_fullscreen()
                
                self.screen.blit(self.game_surface, self.game_surface_centering_coordinates)
                

                pygame.display.flip()
                pygame.event.pump()
                self.clock.tick(self.fps)
                pygame.display.set_caption(f'DC {self.clock.get_fps():.2f}')