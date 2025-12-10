import pygame
from math import ceil, sqrt
from typing import List, Dict, Tuple
from config import config

class RenderEngineEx():
    def __init__(self, screen, screen_center, sprite_group, player):
        # Screen / camera
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.screen_rect = self.screen.get_rect()
        self.screen_center = screen_center
        self.world_space_origin = pygame.Vector2(self.screen_center)
        self.camera_offset = pygame.Vector2(0, 0)
        self.camera_angle = 0
        self.local_rotation = 0
        self.perspective_strength = 8

        # Caches
        self.slice_cache: Dict[Tuple[int,int,int], List[pygame.Surface]] = {}
        self.total_layers = None

        # Sprites
        self.group = sprite_group
        self.player = player
        
        # --- Shadow setup ---
        self.shadow_layer = pygame.Surface(self.screen.get_size(), flags=pygame.SRCALPHA)
        self.shadow_blob_12 = self._make_shadow_blob(diameter=12, alpha=110)  # tweak alpha to taste
        self.shadow_radius = 6  # convenience (diameter // 2)
        
        '''
        # Shadows
        self.enable_shadows = True
        self.light_dir = pygame.Vector2(1, 1).normalize()  # 45° down-right
        self.shadow_alpha = 110                             # opacity
        self.shadow_flatten = 0.55                          # 0..1: “squash” the slice
        self.shadow_px_per_layer = 2.0                      # how far each higher slice’s shadow moves
        '''
    

    

    # ---------- Slicing (NO padding/overdraw) ----------
    def get_slices(self, sheet):
        slice_len = min(sheet.get_width(), sheet.get_height())
        slices = []
        for i in range(sheet.get_width() // slice_len):
            rect = pygame.Rect(i * slice_len, 0, slice_len, slice_len)
            image = sheet.subsurface(rect).copy().convert_alpha()
            slices.append(image)
        self.total_layers = len(slices)
        return slices

    def get_slices_cached(self, sheet):
        # cache key no longer depends on pad
        key = (id(sheet), sheet.get_width(), sheet.get_height())
        cached = self.slice_cache.get(key)
        if cached is None:
            cached = self.get_slices(sheet)
            self.slice_cache[key] = cached
        return cached

    def is_surface_empty(self, s: pygame.Surface) -> bool:
        return s.get_bounding_rect().width == 0

    # ---------- Sorting ----------
    def depth_key(self, sprite):
        if self.player:
            cx, cy = self.player.hitbox.center
        else:
            cx, cy = self.screen_center
        scx, scy = sprite.hitbox.center
        dx = scx - cx
        dy = scy - cy
        return -(dx*dx + dy*dy)
    
    def visible(self, group):

        sprite_group_visible = []  # init once

        for sprite in group:
            sprite_compare_rect = self.world_rect_to_screen(sprite.hitbox)
            if self.screen_rect.colliderect(sprite_compare_rect):
                sprite_group_visible.append(sprite)

        # Draw cast shadow for players and enemies 
        if sprite_group_visible and sprite.sprite_type in ('player', 'enemy'):
            blob = self.shadow_blob_12
            r = self.shadow_radius
            for spr in sprite_group_visible:
                # world -> screen once; hitbox center is your anchor
                sx, sy = self.world_to_screen(spr.hitbox.center)
                self.screen.blit(
                    blob,
                    (int(sx) - r, int(sy) - r),
                    #special_flags=pygame.BLEND_RGBA_MULT  # overlap doesn't darken
        )


        if sprite_group_visible:
            self.sort_sprites_by_distance_from_center(sprite_group_visible, sprite_type= sprite.sprite_type)

    def sort_sprites_by_distance_from_center(self, sprite_group, overdraw_px=0, debug_hitbox=None, sprite_type='default'):
        # NOTE: overdraw_px kept in signature for compatibility; it does nothing now.

        for sprite in sorted(sprite_group, key=self.depth_key):

            dbg_hb = debug_hitbox if debug_hitbox is not None else getattr(sprite, "hitbox", None)
            c = pygame.Vector2(sprite.hitbox.center)
            angle = self.local_rotation
            if sprite_type == 'player':
                angle = -config['controls']['mouse_angle']

            src = getattr(sprite, "image_master", None) or getattr(sprite, "sheet", None) or sprite.image
            self.slice_and_stack(
                c.x, c.y, src,
                local_rotation_angle=angle,
                height=1.0,
                overdraw_px=0,
                debug=False,
                debug_hitbox=dbg_hb,
                fixed_canvas=None,
                rotating=0,
                sprite_type=sprite_type
            )

    # ---------- Space transforms ----------
    
    def world_to_screen(self, world_pos, rect = False):
        '''
        Snap positions here once (int rounding)
        points only
        '''
        v = pygame.Vector2(world_pos) - self.camera_offset
        v.x = int(round(v.x))
        v.y = int(round(v.y))
        return v
    
    def world_rect_to_screen(self, r):
        # r: Rect or FRect in WORLD coords -> returns same type in SCREEN coords
        out = r.copy()
        out.x = int(round(out.x - self.camera_offset.x))
        out.y = int(round(out.y - self.camera_offset.y))
        return out
    
    def screen_to_world(self, screen_pos):
        return pygame.Vector2(screen_pos) + self.camera_offset

    def get_focus_world(self):
        return self.screen_to_world(self.screen_center)

    def get_current_offset(self):
        if not self.player:
            return
        player_center = pygame.Vector2(self.player.hitbox.center)
        self.camera_offset = player_center - self.world_space_origin

    # ---------- Perspective (precompute once per sprite) ----------
    def _precompute_perspective(self, base_world_xy, total_layers, height, sprite_type = 'default'):
        """
        Returns (dir_unit, radial_base, aspect_y_scale, dist_world)
        - dir_unit: unit direction in screen-normalized space
        - radial_base: magnitude factor in [0, ...] based on how far from center (0..1)
        - aspect_y_scale: 1.0 (no special Y)
        - dist_world: raw world-space distance (kept for optional effects)
        """
        focus_world = self.get_focus_world()
        delta = pygame.Vector2(base_world_xy) - pygame.Vector2(focus_world)

        w, h = self.screen_size
        if w == 0 or h == 0:
            return pygame.Vector2(), 0.0, 1.0, 0.0

        # Screen-normalized vector (center -> edges ~ 1.0)
        v = pygame.Vector2(delta.x / (w * 0.5), delta.y / (h * 0.5))

        r = v.length()               # 0 at center, grows radially
        if r > 1.0:
            r = 1.0                  # clamp at edges so far-away stuff doesn’t explode

        dir_unit = v.normalize() if r > 0 else pygame.Vector2()

        # Optional shaping curve (1.0 = linear; >1 = softer near center; <1 = stronger near center)
        curve = getattr(self, "perspective_curve", 1.0)
        r_scaled = r ** curve

        tl = max(total_layers, 1)
        radial_base = self.perspective_strength * (height / tl) * r_scaled

        # --- group-specific adjustments ---
        if sprite_type == 'player':
            # Example: make player offset weaker/stronger
            radial_base -= 0.24   # halve the effect
            dir_unit = pygame.Vector2(0, 1)
            # Or: radial_base += 5  # fixed vertical push

        return dir_unit, radial_base

    def _make_shadow_blob(self, diameter=12, alpha=110) -> pygame.Surface:
        surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, (0, 0, 0, alpha), surf.get_rect())
        return surf
    # ---------- Draw ----------
    def slice_and_stack(
        self,
        x, y, sprite_image,
        local_rotation_angle=0,
        height=1.0,
        overdraw_px=0,                     # kept for compatibility; unused
        debug=False,
        debug_hitbox=None,
        fixed_canvas: pygame.Surface | None = None,  # kept for compatibility; unused
        rotating=0, 
        sprite_type='default'
    ):
   
        slices = self.get_slices_cached(sprite_image)
        total_layers = len(slices)
        if total_layers == 0:
            return

        sprite_world = pygame.Vector2(x, y)

        # Early whole-sprite cull (cheap) using base position + a small padding.
        base_sp = self.world_to_screen(sprite_world)
        # half-diagonal of one slice as cheap radius
        slice_len = min(sprite_image.get_width(), sprite_image.get_height())
        approx_radius = int(slice_len * 0.7071)
        if not self.screen_rect.inflate(approx_radius * 2, approx_radius * 2).collidepoint(base_sp.x, base_sp.y):
            return  # nothing to draw

        # Precompute perspective once
        dir_unit, radial_base = self._precompute_perspective(
            (x, y), total_layers, height, sprite_type = sprite_type
        )

        # Local debug rect (unchanged logic)
        self.debug_draw = debug
        self.debug_colors = {
            "game_hitbox":   (0, 255, 0),
            "render_hitbox": (255, 0, 255),
            "draw_rect":     (255, 215, 0),
        }

        render_hitbox = pygame.FRect(center=(sprite_world.x, sprite_world.y), size=(2, 2))


        sw, sh = self.screen_rect.size
        # Main layer loop — direct blit
        for i, layer in enumerate(slices):
            if self.is_surface_empty(layer):
                continue

            # Per-layer perspective offset via cached scalars
            off_x = dir_unit.x * radial_base * i
            off_y = dir_unit.y * radial_base * i * (total_layers * 0.1)
            layer_world = (sprite_world.x + off_x, sprite_world.y + off_y)

            sp = self.world_to_screen(layer_world)

            rotated_layer = pygame.transform.rotate(layer, local_rotation_angle)
            lr = rotated_layer.get_rect(center=(sp.x, sp.y))
            self.screen.blit(rotated_layer, lr)

            if i == 0:
                ow, oh = layer.get_size()
                render_hitbox.width, render_hitbox.height = ow, oh
                render_hitbox.center = sprite_world
