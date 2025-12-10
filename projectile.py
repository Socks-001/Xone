import pygame
import math
import random
from weapon_data import weapons
from level_data import level
from config import config 
from sfx import sfx
from light import Light


class Projectile(pygame.sprite.Sprite):
    def __init__(self, owner, owner_sprite_type, groups, shoot_direction, weapon_name):

        super().__init__(groups)	
        self.owner = owner
        self.owner_sprite_type = owner_sprite_type # differentiates player/enemy
        self.direction = shoot_direction.normalize() # direction to shoot
        self.SCREEN_WIDTH = config['screen']['SCREEN_WIDTH']

        # Weapon Data (Dynamic)
        self.sprite_type = 'projectile'
        weapon_data = weapons[weapon_name]
        self.accuracy = weapon_data['accuracy']
        self.attack_damage = weapon_data['damage']
        self.sprite = weapon_data['sprite']
        self.velocity = float(weapon_data['speed']) # Speed projectile travles at 
        self.shot_sound = sfx['weapon']['shot'] # Sound of the weapon, temporary sound, will update per weapon
        self.lifetime = pygame.time.get_ticks()

        # Image and Rect 
        angle = math.degrees(math.atan2(-self.direction.y, self.direction.x))
        self.image = pygame.transform.rotate(self.sprite, angle)
        self.rect = self.image.get_rect(center=self.owner.rect.center)
        self.hitbox = pygame.FRect(self.rect)
        #movement varialbles
        self.previous_position = (0,0)
        self.current_position = (0,0)
        self.debug_ray_paths = []  # For debug purposes

        # Obstacle and Entity reference 
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        self.offset_applied = False
        
        # Trail-related attributes
        self.trail_positions = []  # List of previous positions
        self.trail_length = 10  # Number of trail elements
        self.trail_image = self.image.copy()  # Image for the trail

        #sound
        self.shot_sound.play()  # Play the shot sound
     
       #tracer
        #self.tracer = Light(self.hitbox.center, level['sprite_groups']['light_sprites'], '53', self)

    def calculate_angle_offset(self):
        """Applies a small random angular offset to the projectile's trajectory."""
        
        offset = self.accuracy  # Max random offset
        
        # Generate a single random offset within the accuracy range
        offset_angle = random.uniform(-offset, offset)

        # Get the current movement direction's angle
        angle = math.atan2(self.direction.y, self.direction.x)

        # Apply the offset
        new_angle = angle + offset_angle

        # Convert back to a movement vector
        self.direction = pygame.math.Vector2(math.cos(new_angle), math.sin(new_angle))
        self.offset_applied = True

    def move_projectile(self, velocity):
        self.previous_position = tuple(self.hitbox.center)
        # Move the projectile in the adjusted direction
        self.hitbox.x += self.direction.x * velocity
        self.hitbox.y += self.direction.y * velocity
        self.rect.center = self.hitbox.center
        self.current_position = tuple(self.hitbox.center)

                # Update trail
        self.trail_positions.insert(0, self.rect.center)
        if len(self.trail_positions) > self.trail_length:  # Limit trail length
            self.trail_positions.pop()

        """Returns a rect representing the swept path of the projectile (covers tunneling)."""
        start = pygame.math.Vector2(self.previous_position)
        end = pygame.math.Vector2(self.current_position)
        direction = end - start
        length = direction.length()

        if length == 0:
            return pygame.Rect(start.x, start.y, 1, 1)

        width = self.rect.width  # Use projectile's width
        center = start.lerp(end, 0.5)

        # Create an axis-aligned rect spanning the movement with width
        # We'll align it horizontally or vertically based on the greater axis
        if abs(direction.x) > abs(direction.y):
            motion_rect = pygame.Rect(0, 0, length, width)
        else:
            motion_rect = pygame.Rect(0, 0, width, length)

        motion_rect.center = center
        return motion_rect

    def lifetime_check(self):
        if pygame.time.get_ticks() - self.lifetime > 5000:  # 1 second, lifetime of projectile
            self.kill()

    def check_collision(self):
        start = pygame.Vector2(self.previous_position)
        end = pygame.Vector2(self.current_position)
        direction = (end - start).normalize()
        normal = pygame.Vector2(-direction.y, direction.x)  # Perpendicular vector

        # Adjust this to increase/decrease thickness
        offset_distance = self.rect.width / 2

        # Three raycasts
        ray_paths = [
            (start, end),  # center
            (start + normal * offset_distance, end + normal * offset_distance),  # left
            (start - normal * offset_distance, end - normal * offset_distance),  # right
        ]

        # in check_collision()
        self.debug_ray_paths = ray_paths

        # Check entity collisions
        for entity in self.entity_sprites:
            if entity.sprite_type != self.owner_sprite_type:
                for ray_start, ray_end in ray_paths:
                    if entity.hitbox.clipline(ray_start, ray_end):
                        if entity.vulnerable:
                            entity.take_damage(self.attack_damage)
                            self.kill()
                        else:
                            entity.take_hit_no_damage()
                            self.kill()
                        
                        return

        # Check obstacle collisions
        for sprite in self.obstacle_sprites:
            for ray_start, ray_end in ray_paths:
                if sprite.rect.clipline(ray_start, ray_end):
                    self.kill()
                    return
        '''
        # Check bounds
        if (
            self.hitbox.x > self.SCREEN_WIDTH or 
            self.hitbox.x < 0 or
            self.hitbox.y > config['screen']['SCREEN_HEIGHT'] or
            self.hitbox.y < 0
        ):
            self.kill()
        '''

    
    def draw(self, surface, debug_bool = True):
        """Call this manually from your main draw loop if using custom rendering."""
        # Draw trail
        for i, pos in enumerate(self.trail_positions):
            fade_strength = (1 - i / len(self.trail_positions)) ** 2
            alpha = int(255 * fade_strength)
            

            # Create a copy of the image to modify for the trail (so we don't change the original sprite)
            self.trail_image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)

            # Apply color (only affecting the trail)
            self.trail_image.fill(config['color_list']['neon_green'])
            self.trail_image.set_alpha(alpha)

            # Now place the faded image with the red tint on the trail position
            #trail_FRect = pygame.FRect(center=pos, size=self.trail_image.get_size())
            rect = self.trail_image.get_rect(center=pos)
            surface.blit(self.trail_image, rect.topleft)

        # Draw the main projectile (no changes to the original sprite)
        surface.blit(self.image, self.rect.topleft)

        if debug_bool:
            color = (255, 255, 0)
            for ray_start, ray_end in self.debug_ray_paths:
                pygame.draw.line(surface, color, ray_start, ray_end, 1)

    def update(self):
        # Update obstacle and entity references
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        if self.offset_applied is False:
            self.calculate_angle_offset()
        self.move_projectile(self.velocity)
        self.check_collision()
        self.lifetime_check()

        #Treasure of the Rudras SNES Art
        #Shadownrun SNES