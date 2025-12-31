import pygame
from level_instancer import Game
from menu import Menu
from config import config
from level_data import level
from controls import Controls
from debug import sprite_group_highlight
from utilities import draw_point, get_surface_center
from render_engine_ex import RenderEngineEx
import spatial_index


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
        pygame.display.set_caption('DC')

        # Game
        self.controls = Controls()
        self.game = Game(self.controls)
        level['level_config']['game'] = self.game

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
        from player_data import player_data

        p = player_data.get("player")

        # If the player is gone (dead/permadeath/menu transition), mark world not ready.
        if p is None:
            self.world_ready = False
            self.render_engine.player = None
            return

        # Bind once or rebind if replaced
        if (not self.world_ready) or (self.render_engine.player is not p):
            self.render_engine.player = p
            self.world_ready = True


    def get_sprite_groups_from_dict(self):
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.weapon_sprites = level['sprite_groups']['weapons_sprites']
        self.player_sprites = level['sprite_groups']['player_sprites']
        self.enemy_sprites = level['sprite_groups']['enemy_sprites']
        self.set_dressing_sprites = level['sprite_groups']['set_dressing_sprites']
        self.floor_sprites = level['sprite_groups']['floor_sprites']
        self.wall_sprites = level['sprite_groups']['wall_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        self.light_sprites = level['sprite_groups']['light_sprites']
        self.dynamic_sprites = level['sprite_groups']['dynamic_sprites']
        
    
    def update_sprite_groups(self, dt):
        self.dynamic_sprites.update(dt)
        
        dyn = level['current']['dynamic_index']
        for spr in self.dynamic_sprites:
            moved = getattr(spr, "_moved", True)
            if moved:
                dyn.update(spr)
                if hasattr(spr, "_moved"):
                    spr._moved = False

        

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

    def draw_game_scene(self, debug, dt):
        # --- in draw_game_scene() at the very top ---
        
        self.get_sprite_groups_from_dict()
        self.ensure_stacker_player()
        
        # Get Index Lists 
        static_index = level['current']['static_index']
        dynamic_index = level['current']['dynamic_index']
        

        if not self.world_ready:
            return  # no player yet; skip this frame cleanly
        
        self.game_surface.fill(config['ui']['colors']['BG_COLOR'])
        self.update_sprite_groups(dt)
        self.debug_bool = config['debug']['projectile_lines']

        # Get offset, camera, then query buckets against camera
        self.render_engine.get_current_offset()
        camera = self.render_engine.world_camera_rect
        static_candidates = static_index.query_rect(camera)
        dynamic_candidates = dynamic_index.query_rect(camera)
        
        dynamic_candidates = [s for s in dynamic_candidates if s.alive()]


        # --- Partition static candidates (floor / foliage / other) ---
        floors, foliage, static_other = [], [], []

        for s in static_candidates:
            t = getattr(s, "sprite_type", None)
            if t == "floor":
                floors.append(s)
            elif t == "set_dressing":
                foliage.append(s)
            else:
                static_other.append(s)

        # --- Render order ---
        # 1) floor
        # 2) foliage (current set_dressing/grass)
        # 3) everything else together (walls + entities + projectiles + lights)
        self.render_engine.visible(floors)
        self.render_engine.visible(foliage)

        combined = static_other + dynamic_candidates
        self.render_engine.visible(combined)

        pc = pygame.Vector2(getattr(self.render_engine, "last_player_center",
                            self.render_engine.player.hitbox.center))

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
                
				# Compute delta time
                self.clock.tick(0)
                frame_dt = self.clock.get_rawtime() / 1000.0
                if frame_dt > 0.05:
                    frame_dt = 0.05

                if config['menu']['menu_running']:
                    self.menu.update(action_map, self.game_surface)
                else:
                   self.draw_game_scene(debug=config['debug']['debug'], dt=frame_dt)

                # Handle scaling and fullscreen changes
                self.handle_fullscreen()
                
                self.screen.blit(self.game_surface, self.game_surface_centering_coordinates)
                

                pygame.display.flip()
                pygame.event.pump()
                inst_fps = (1.0 / frame_dt) if frame_dt > 0 else 0.0
                pygame.display.set_caption(
                    f'DC avg {self.clock.get_fps():.1f} | inst {inst_fps:.1f}'
                )

