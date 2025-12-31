import pygame
import random
import math
from config import config
from light_data import light_types

class Light(pygame.sprite.Sprite):
    def __init__(self, pos, groups, light_config_index, follow_target = None):
        super().__init__(groups)

        # configure light variables
        self.light_type = light_types[light_config_index]
        self.sprite_type = self.light_type['sprite_type']
        self.type = self.light_type['type']
        self.shape = self.light_type['shape']
        self.draw_shape = self.light_type['draw_shape']
        self.radius = self.light_type['radius']
        self.color = self.light_type['color']
        self.time = 0.0
        self.follow = follow_target
        
        self.flicker = self.light_type.get('flicker', False)
        if self.flicker:
            self.flicker_timer = 0.0
            self.flicker_interval = random.uniform(0.05, 1.5)

        self.ebb = self.light_type.get('ebb', False)
        if self.light_type['ebb']:
            self.ebb_frequency = self.light_type.get('ebb_frequency', 0.1)
    
        self.decay = self.light_type.get('decay', None)

        self.alpha = self.light_type.get('alpha', 180)
    
        self.complete_color = (self.color,self.alpha)

        self.shift = self.light_type.get('shift', False)

        if self.shape == 'circle':        
            self.image = self.generate_radial_gradient(self.radius, self.color, self.alpha)

        
        # set position on map
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.FRect(self.rect)
        self._moved = True
        self.z = 0.0
        self.z_height = config['render']['Z_UNIT']

    def generate_radial_gradient(self, radius, color, alpha):
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)  # Create a transparent surface

            for y in range(radius * 2):  # For each row
                for x in range(radius * 2):  # For each column
                    dx = x - radius  # Horizontal distance from center
                    dy = y - radius  # Vertical distance from center
                    distance = math.hypot(dx, dy)  # Euclidean distance from center

                    if distance <= radius:  # If the pixel is inside the light radius
                        falloff = 1 - (distance / radius)  # How close it is to the center (1 at center, 0 at edge)
                        a = int(alpha * (falloff ** 2))  # Use a curve (quadratic) for smoother fade
                        surf.set_at((x, y), (*color, a))  # Set the pixel's color and alpha

            return surf
        
        
    
    def update(self, dt=0.0):
        dt_scale = dt * config['screen']['LOGIC_FPS']
        if self.shift and self.shift != (0, 0):
            self.rect.topleft = (self.rect.topleft[0] + self.shift[0] * dt_scale,
                                 self.rect.topleft[1] + self.shift[1] * dt_scale)
            self._moved = True
        
        if self.follow:
            self.hitbox.center = self.follow.hitbox.center
            self.rect.center = self.hitbox.center
            self.z = getattr(self.follow, "z", self.z)
            self._moved = True

        # Flicker behavior
        if self.flicker:
            self.flicker_timer += dt
            if self.flicker_timer >= self.flicker_interval:
                self.flicker_timer = 0.0
                self.flicker_interval = random.uniform(0.05, 0.5)
                # Random small fluctuations
                flicker_variation = random.randint(-30, 30)
                flicker_alpha = max(100, min(255, self.alpha + flicker_variation))
                flicker_color = tuple(max(0, min(255, c + random.randint(-15, 15))) for c in self.color)
                self.image.fill((0, 0, 0, 0))  # Clear surface
                self.image = self.generate_radial_gradient(self.radius, flicker_color, flicker_alpha)

        # Ebb behavior (sine wave)
        elif self.ebb:
            wave = (math.sin(self.time * self.ebb_frequency) + 1) / 2  # Normalize to 0–1
            ebb_alpha = int(100 + (self.alpha - 100) * wave)
            ebb_color = tuple(int(50 + (c - 50) * wave) for c in self.color)
            self.image.fill((0, 0, 0, 0))  # Clear surface
            self.image = self.generate_radial_gradient (self.radius, ebb_color, ebb_alpha)
            self.time += dt

        # If no flicker or ebb, static light
        else:
            pass
