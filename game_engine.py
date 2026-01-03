import math
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
        # 1) floor surface
        # 2) foliage (current set_dressing/grass)
        # 3) everything else together (walls + entities + projectiles + lights)
        self.draw_floor_surface()
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

        if debug == True and config['debug'].get('vision_cones', False):
            self.draw_vision_cones()

        self.draw_scale_mode()

    def draw_scale_mode(self):
        self.font = pygame.font.SysFont("atkinsonhyperlegiblemonoextralight", 12)
        color = (255, 20, 147)
        label = "scale: linear"
        text_surface = self.font.render(label, True, color)
        text_rect = text_surface.get_rect(bottomright=(self.game_surface.get_width() - 6,
                                                       self.game_surface.get_height() - 6))
        self.game_surface.blit(text_surface, text_rect)

        cam_z = getattr(self.render_engine, "camera_z", 0.0)
        cam_label = f"cam_z: {cam_z:.2f}"
        cam_surface = self.font.render(cam_label, True, color)
        cam_rect = cam_surface.get_rect(bottomright=(self.game_surface.get_width() - 6,
                                                     self.game_surface.get_height() - 22))
        self.game_surface.blit(cam_surface, cam_rect)

    def draw_vision_cones(self):
        overlay = getattr(self, "_vision_overlay", None)
        if overlay is None or overlay.get_size() != self.game_surface.get_size():
            self._vision_overlay = pygame.Surface(self.game_surface.get_size(), flags=pygame.SRCALPHA)
            overlay = self._vision_overlay

        overlay.fill((0, 0, 0, 0))
        color = (255, 20, 147, 80)

        for enemy in self.enemy_sprites:
            if not enemy.alive():
                continue
            forward = getattr(enemy, "facing_dir", pygame.Vector2())
            if forward.length_squared() == 0:
                continue
            forward = forward.normalize()

            vision_range = max(getattr(enemy, "vision_range", 0.0), getattr(enemy, "vision_min_range", 1.0))
            base_radius = getattr(enemy, "vision_base_radius", 8.0)
            half_angle = math.atan2(base_radius, vision_range)
            angle_deg = math.degrees(half_angle)
            left = forward.rotate(angle_deg)
            right = forward.rotate(-angle_deg)

            origin = pygame.Vector2(enemy.hitbox.center)
            p1 = origin + (left * vision_range)
            p2 = origin + (right * vision_range)

            scale = self.render_engine.get_scale_for_sprite(enemy)
            o_sp = self.render_engine.world_to_screen_scaled(origin, scale)
            p1_sp = self.render_engine.world_to_screen_scaled(p1, scale)
            p2_sp = self.render_engine.world_to_screen_scaled(p2, scale)

            pygame.draw.polygon(overlay, color, [o_sp, p1_sp, p2_sp])

        self.game_surface.blit(overlay, (0, 0))

    def draw_floor_surface(self):
        floor_surface = level['current'].get('floor_surface')
        if floor_surface is None:
            return
        scale = self.render_engine.get_scale_for_z(0.0)
        cache = level['current'].get('floor_surface_cache', {})
        scaled = cache.get(scale)
        if scaled is None:
            w = max(1, int(round(floor_surface.get_width() * scale)))
            h = max(1, int(round(floor_surface.get_height() * scale)))
            scaled = pygame.transform.scale(floor_surface, (w, h))
            cache[scale] = scaled
            level['current']['floor_surface_cache'] = cache
        top_left = self.render_engine.world_to_screen_scaled((0, 0), scale)
        self.game_surface.blit(scaled, top_left)
            
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

