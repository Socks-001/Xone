import pygame
import math
import random
from weapon_data import weapons
from level_data import level
from config import config 

pygame.init()

class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner, owner_sprite_type, groups, shoot_direction, weapon_name):

        super().__init__(groups)	
        self.owner = owner
        self.owner_sprite_type = owner_sprite_type # differentiates player/enemy
        self.direction = shoot_direction.normalize() # direction to shoot
        self.SCREEN_WIDTH = config['screen']['SCREEN_WIDTH']

        # Weapon Data (Dynamic)
        weapon_data = weapons[weapon_name]
        self.accuracy = weapon_data['accuracy']
        self.attack_damage = weapon_data['damage']
        self.sprite = weapon_data['sprite']
        self.velocity = float(weapon_data['speed']) # Speed projectile travles at 
        self.shot_sound = weapons['sound'] # Sound of the weapon, temporary sound, will update per weapon
        self.lifetime = pygame.time.get_ticks()

        # Image and Rect 
        self.image = self.sprite  # Load sprite
        self.rect = self.image.get_rect(center=self.owner.rect.center)
        self.projectile_hitbox = pygame.FRect(self.rect)

        # Obstacle and Entity reference 
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        self.offset_done = None
        
        # Trail-related attributes
        self.trail_positions = []  # List of previous positions

        self.shot_sound.play()  # Play the shot sound
        self.previous_position = (0,0)
        self.current_position = (0,0)

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
        self.offset_done = 1

    def move_projectile(self, velocity):
        self.previous_position = tuple(self.projectile_hitbox.center)
        # Move the projectile in the adjusted direction
        self.projectile_hitbox.x += self.direction.x * velocity
        self.projectile_hitbox.y += self.direction.y * velocity
        self.rect.center = self.projectile_hitbox.center
        self.current_position = tuple(self.projectile_hitbox.center)

                # Update trail
        self.trail_positions.insert(0, self.rect.center)
        if len(self.trail_positions) > 18:  # Limit trail length
            self.trail_positions.pop()

    def lifetime_check(self):
        if pygame.time.get_ticks() - self.lifetime > 5000:  # 1 second, lifetime of projectile
            self.kill()

    def check_collision(self):
        # Check collisions with entities
        for entity in self.entity_sprites:
            # Create a line segment from the previous position to the current position
            if entity.hitbox.clipline(self.previous_position, self.current_position):
                # Check if the entity is of a different sprite type (not the owner)
                if entity.sprite_type != self.owner_sprite_type:
                    if entity.vulnerable:
                        entity.take_damage(self.attack_damage)  # Apply damage
                        entity.vulnerable = False  # Entity becomes invulnerable after being hit
                        self.kill()  # Destroy the projectile
                        return  # Exit after the first collision
                  
                    else:
                        entity.take_hit_no_damage()
                        self.kill()

        # Check collisions with obstacles
        for sprite in self.obstacle_sprites:
            if sprite.rect.clipline(self.previous_position, self.current_position):
                self.kill()
                return
        
        if (self.projectile_hitbox.x > self.SCREEN_WIDTH or self.projectile_hitbox.x < 0 or self.projectile_hitbox.y > config['screen']['SCREEN_HEIGHT'] or self.projectile_hitbox.y < 0):
            self.kill()
    
    def draw(self, surface, debug = False):
        """Call this manually from your main draw loop if using custom rendering."""
        # Draw trail
        for i, pos in enumerate((self.trail_positions)):
            alpha = int(100 * (1 - i / 18))  # Decrease alpha with age
            faded_image = self.image.copy()
            faded_image.set_alpha(alpha)
            rect = faded_image.get_rect(center=pos)
            surface.blit(faded_image, rect.topleft)

        # Draw main projectile
        surface.blit(self.image, self.rect.topleft)

        if debug:
            # Draw the previous and current positions for debugging
            pygame.draw.line(surface, (255, 255, 0), self.previous_position, self.current_position, 5)  # Yellow line


    def update(self):
        # Update obstacle and entity references
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']
        if self.offset_done == None:
            self.calculate_angle_offset()
        self.move_projectile(self.velocity)
        self.check_collision()
        self.lifetime_check()

        #Treasure of the Rudras SNES Art
        #Shadownrun SNES