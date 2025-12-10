import pygame
from math import ceil, sqrt 
from typing import List, Dict, Tuple 
            
class RenderEngineEx():
    def __init__(self, screen, screen_center, sprite_group, player):

        #Screen Setup - Screen is actually refering to target render surface not necessarily the main screen surface
        self.screen = screen
        self.screen_size = self.screen.get_size()
        self.screen_rect = self.screen.get_rect()

        #Slicing Sprites
        self.slice_cache: Dict[Tuple[int,int,int,int], List[pygame.Surface]] = {} # key: (id(surface), w, h) -> list[Surface]
        self.total_layers = None

        #Larger surface for centering
        self.dim_cache: dict[tuple[int,int], int] = {}     # (slice_len, pad) -> max_dim
        self.canvas_by_dim: dict[int, pygame.Surface] = {} # dim -> reusable Surface

        #Camera
        w, h = self.screen_size
        self.screen_center = screen_center
        self.world_space_origin = pygame.Vector2(self.screen_center) #World space origin
        self.camera_offset = pygame.Vector2(0, 0) #distance camera is from origin
        self.camera_angle = 0
        self.local_rotation = 0
        self.perspective_strength = 20

        #Get sprite group
        self.group = sprite_group
        self.player = player 

   
       
    # ---------- Slicing ----------
    def get_slices(self, sheet, pad: int = 0):
        slice_len = min(sheet.get_width(), sheet.get_height())
        slices = []
        for i in range(sheet.get_width() // slice_len):
            rect = pygame.Rect(i * slice_len, 0, slice_len, slice_len)
            image = sheet.subsurface(rect).copy()
            if pad:
                image = self.extrude(image, pad)
            slices.append(image)
        self.total_layers = len(slices)
        return slices  
    
    def get_slices_cached(self, sheet, pad: int = 0):
        key = (id(sheet), sheet.get_width(), sheet.get_height(), pad)  # include pad in key!
        cached = self.slice_cache.get(key)
        if cached is None:
            cached = self.get_slices(sheet, pad)
            self.slice_cache[key] = cached
        return cached 
    
    def extrude(self, surf: pygame.Surface, pad: int = 1) -> pygame.Surface:
        if pad <= 0:
            return surf
        w, h = surf.get_size()
        out = pygame.Surface((w + 2*pad, h + 2*pad), pygame.SRCALPHA)
        # center
        out.blit(surf, (pad, pad))
        # edges
        out.blit(surf.subsurface((0, 0, 1, h)),        (0, pad))          # left
        out.blit(surf.subsurface((w-1, 0, 1, h)),      (pad + w, pad))    # right
        out.blit(surf.subsurface((0, 0, w, 1)),        (pad, 0))          # top
        out.blit(surf.subsurface((0, h-1, w, 1)),      (pad, pad + h))    # bottom
        # corners
        out.blit(surf.subsurface((0, 0, 1, 1)),        (0, 0))
        out.blit(surf.subsurface((w-1, 0, 1, 1)),      (pad + w, 0))
        out.blit(surf.subsurface((0, h-1, 1, 1)),      (0, pad + h))
        out.blit(surf.subsurface((w-1, h-1, 1, 1)),    (pad + w, pad + h))
        return out
    
    def is_surface_empty(self, s: pygame.Surface) -> bool:
        return s.get_bounding_rect().width == 0  # empty (all transparent)
    
    def depth_key(self, sprite):
        if not self.player:
            cx, cy = self.screen_center
        else:
            cx, cy = self.player.hitbox.center

        # base slice length = min(w, h)
        sprite_center = pygame.Vector2(sprite.hitbox.center)
        scx, scy = sprite_center
        dx, dy = (scx - cx), (scy - cy)
        return -(dx*dx + dy*dy)

    def sort_sprites_by_distance_from_center(self, sprite_group, overdraw_px=0, debug_hitbox=None):
        for sprite in sorted(sprite_group, key=self.depth_key):
            dbg_hb = debug_hitbox if debug_hitbox is not None else getattr(sprite, "hitbox", None)

            # Use world-aware center (handles wide sheets correctly)
            c = pygame.Vector2(sprite.hitbox.center)

            # Per your rule: floors/walls get pad=2, others use passed arg
            pad = 2 if getattr(sprite, "sprite_type", "") in ("floor", "wall") else overdraw_px

            # Figure out base slice size from the image
            w, h = sprite.image.get_size()
            slice_len = min(w, h)

            # Get (and cache) the max rotated dim, then get a reusable canvas
            dim = self._max_rotated_dim(slice_len, pad)
            canvas = self._get_canvas(dim)
           

            # Call your renderer, but switch it to accept a preallocated canvas
            self.slice_and_stack(
                c.x, c.y, sprite.image,
                local_rotation_angle = self.local_rotation,
                overdraw_px=pad,
                debug_hitbox=dbg_hb,
                fixed_canvas=canvas,   # <— see change below
            )
        
    def frect_from_center(self, center: pygame.Vector2, w: float, h: float) -> pygame.FRect:
        return pygame.FRect(center = (center.x, center.y), width = w, height = h)
       
    def _max_rotated_dim(self, slice_len: int, pad: int) -> int:
        # worst-case bound for a square slice after rotation, including pad
        s = slice_len + 2*pad
        key = (s, 0)
        d = self.dim_cache.get(key)
        if d is None:
            d = ceil(s * sqrt(2))  # ceil(sqrt(s^2 + s^2))
            self.dim_cache[key] = d
        return d

    def _get_canvas(self, dim: int) -> pygame.Surface:
        surf = self.canvas_by_dim.get(dim)
        if surf is None:
            surf = pygame.Surface((dim, dim), pygame.SRCALPHA)
            self.canvas_by_dim[dim] = surf
        return surf
    # ---------- Space transforms ----------

    def world_to_screen(self, world_pos):
        return pygame.Vector2(world_pos) - self.camera_offset
    
    # ---------- Perspective ----------
    
    def get_perspective_offset(self, surface_pos, focus_point, layer_index, stack_object_height, total_layers=None):
        """Compute per-layer radial offset in *view space*."""
       
        if total_layers is None:
            total_layers = self.total_layers

        
        direction = pygame.Vector2(surface_pos) - pygame.Vector2(focus_point)
       
        if direction.length() == 0:    
            return (0, 0)
         
        else: 
            # Cap the distance to prevent extreme distortion
            screen_w, screen_h = self.screen_size
            max_dimension = max(screen_w, screen_h)
            max_distance = max_dimension  # Tune this number as needed
            distance = min(direction.length(), max_distance)
            direction.normalize_ip()

            # Calculate the capped perspective offset magnitude
            radial_mag = self.perspective_strength * (stack_object_height / total_layers) * (distance / (self.screen_size[0] / 2))
            radial_x = (direction.x * radial_mag * layer_index) 
            radial_y = (direction.y * radial_mag * layer_index) 
            
                
            return (radial_x, radial_y)
        
    def apply_rotation_based_on_focus_point(self, pos, pivot, angle_deg):
        v = pygame.Vector2(pos) - pygame.Vector2(pivot)
        v.rotate_ip(angle_deg)
        return pygame.Vector2(pivot) + v
        
    def get_current_offset(self):
        if not self.player:
            return
        player_center = pygame.Vector2(self.player.hitbox.center)
        self.camera_offset = player_center - self.world_space_origin

    def screen_to_world(self, screen_pos):
        # inverse of world_to_screen(world) = world - camera_offset
        return pygame.Vector2(screen_pos) + self.camera_offset

    def get_focus_world(self):
        # if you want the camera focus at the game_surface center (not the player),
        # use the world position that maps to the current screen center
        return self.screen_to_world(self.screen_center)

    def slice_and_stack(self, x, y, sprite_sheet, local_rotation_angle = 0, height=1.0, overdraw_px=0, debug = False, debug_hitbox = None, fixed_canvas : pygame.Surface | None = None):
        
        slices = self.get_slices_cached(sprite_sheet, pad=overdraw_px)
        total_layers = len(slices)
        focus_point = self.get_focus_world()

        # Treat (x, y) as the base anchor in WORLD space
        sprite_world_coords = pygame.Vector2(x, y)

        self.debug_draw = debug
        self.debug_colors = {
        "game_hitbox":   (0, 255, 0),    # green
        "render_hitbox": (255, 0, 255),  # magenta
        "draw_rect":     (255, 215, 0),  # gold
        }       
        
        # Local render rect for this draw only (do NOT mutate any world hitboxes)
        render_hitbox = self.frect_from_center(sprite_world_coords, 2, 2)
   
        for i, layer in enumerate(slices):

            if self.is_surface_empty(layer):
                continue


            #Rotate the scaled layer (never transforming image twice)
            rotated = pygame.transform.rotate(layer, self.camera_angle)

            # pick the canvas (preallocated) and clear it for this layer
            canvas = fixed_canvas if fixed_canvas is not None else self._get_canvas(
                self._max_rotated_dim(min(*layer.get_size()), overdraw_px)
            )
            canvas.fill((0,0,0,0))

            # center the rotated slice on the fixed-size canvas
            cx = (canvas.get_width()  - rotated.get_width())  // 2
            cy = (canvas.get_height() - rotated.get_height()) // 2
            canvas.blit(rotated, (cx, cy))

            #Get radial offset 
            a,b = sprite_world_coords

            offset_x, offset_y = self.get_perspective_offset(
                (a, b), focus_point, i,
                height,
                total_layers=total_layers
            )
    
            
            #Apply offset to coords 
            perspective_offset_position = (
                (a + ( offset_x), 
                b + (offset_y))
                )
            
            #Apply rotation to world coord (persp corrected) based on world space origin
            final_world_position = self.apply_rotation_based_on_focus_point(
                    perspective_offset_position,
                    focus_point,
                    self.camera_angle
                )

            

            #Draw to screen 
            #Transform world space to screen space, self.rect/self.hitbox is at correct world space coords
            
            sp = self.world_to_screen(final_world_position)
            if not self.screen_rect.inflate(64, 64).collidepoint(int(sp.x), int(sp.y)):
                continue
            draw_rect = canvas.get_rect(center=(int(round(sp.x)), int(round(sp.y))))
            self.screen.blit(canvas, draw_rect)

            
             # Base layer: size the LOCAL render rect (debug helper only)
            if i == 0:
                ow, oh = layer.get_size()
                render_hitbox.width, render_hitbox.height = ow, oh
                render_hitbox.center = sprite_world_coords

            