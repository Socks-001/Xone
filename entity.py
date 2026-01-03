import pygame
from config import config
from level_data import level
from player_data import player_data
from enemy_data import enemy_data
from sfx import sfx
from utilities import destroy_sprite, z_ranges_overlap
from particles import AnimationPlayer

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, name):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.sprite_name = name
        self.collision_tolerance = 10
        if self.sprite_type == 'player':
            self.sprite =  player_data['sprite']
        else:
            self.sprite = enemy_data[self.sprite_name]['sprite']
        self.image = self.sprite
        self.sprite_dimensions = self.stack_slice_len(self.image)
        d = self.sprite_dimensions
        self.rect = pygame.Rect((0,0),(d,d))
        self.rect.center = pos
        self.hitbox = pygame.FRect(self.rect)
        self.hitbox.inflate_ip(-4, -4)
        self.direction = pygame.math.Vector2()
        self.z = 0.0
        stack_layers = max(1, int(self.image.get_width() // d))
        self.z_height = config['render']['Z_UNIT'] * stack_layers
        self.z_vel = 0.0
        self._moved = True
        self._ground_z_cached = None
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.weapon_sprites = level['sprite_groups']['weapons_sprites']
        self.dynamic_sprites = level['sprite_groups']['dynamic_sprites']
        self.animation_player = AnimationPlayer()
        self.hit_sound = sfx['entity']['hit']
        self.death_sound = sfx['entity']['death']
        # Set volume to 50%
        
    
      # Vulnerability properties
        self.vulnerable = True  # Entity is initially vulnerable
        self.hit_time = 0  # Time when the entity was last hit
        self.invulnerability_duration = 500  # Time in milliseconds (e.g., 500ms = 0.5 seconds)

    def stack_slice_len(self, surface: pygame.Surface) -> int:
        """Square base size (px) assumed by stacked sheets (min of w/h)."""
        return min(surface.get_width(), surface.get_height())
    
    def get_ground_z(self):
        if not self._moved and self._ground_z_cached is not None:
            return self._ground_z_cached
        static_index = level['current'].get('static_index')
        if static_index is None:
            return None
        candidates = static_index.query_rect(self.hitbox)
        floor_z = None
        z_unit = config['render']['Z_UNIT']
        foot_x, foot_y = self.hitbox.center
        for spr in candidates:
            if getattr(spr, "sprite_type", None) not in ("floor", "floor_upper"):
                continue
            if not spr.rect.colliderect(self.hitbox):
                continue
            base_z = getattr(spr, "z", 0.0)
            ramp_dir = getattr(spr, "ramp_dir", None)
            if ramp_dir:
                left = spr.rect.left
                top = spr.rect.top
                right = spr.rect.right
                bottom = spr.rect.bottom
                if ramp_dir == "left":
                    t = (right - foot_x) / max(1.0, spr.rect.width)
                elif ramp_dir == "right":
                    t = (foot_x - left) / max(1.0, spr.rect.width)
                elif ramp_dir == "up":
                    t = (bottom - foot_y) / max(1.0, spr.rect.height)
                elif ramp_dir == "down":
                    t = (foot_y - top) / max(1.0, spr.rect.height)
                else:
                    t = 0.0
                t = max(0.0, min(1.0, t))
                z = base_z + (t * z_unit)
            else:
                z = base_z
            is_ramp = ramp_dir is not None
            if is_ramp or z <= (self.z + 0.1):
                if floor_z is None or z > floor_z:
                    floor_z = z
        self._ground_z_cached = floor_z
        return floor_z

    def vulnerability_cooldown(self):
        """Handles the cooldown for vulnerability."""
        if not self.vulnerable:
            if pygame.time.get_ticks() - self.hit_time > self.invulnerability_duration:
                self.vulnerable = True  # Entity becomes vulnerable again after the cooldown period

    def apply_gravity(self, dt_scale, ground_z=None):
        if ground_z is None:
            ground_z = self.get_ground_z()

        if config['physics']['gravity'] != 0.0:
            self.z_vel -= config['physics']['gravity'] * dt_scale

        self.z += self.z_vel * dt_scale
        if ground_z is not None and self.z < ground_z:
            self.z = ground_z
            self.z_vel = 0.0

    def move(self, speed):
        prev_center = self.hitbox.center
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        max_step = config['physics']['max_step']
        steps = max(1, int(max(abs(self.direction.x * speed), abs(self.direction.y * speed)) // max_step) + 1)
        step_speed = speed / steps

        for _ in range(steps):
            # Horizontal movement and collision check
            self.hitbox.x += self.direction.x * step_speed
            self.collision('horizontal')

            # Vertical movement and collision check
            self.hitbox.y += self.direction.y * step_speed
            self.collision('vertical')

        # Update rect position after movement
        self.rect.center = self.hitbox.center
        moved = (self.hitbox.center != prev_center)
        self._moved = self._moved or moved

    def collision(self, direction):
        """Handles collision detection and prevents movement through obstacles."""
        for sprite in self.obstacle_sprites:
            if not z_ranges_overlap(self, sprite):
                continue
            if sprite.rect.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # Moving right
                        self.hitbox.right = sprite.rect.left
                    elif self.direction.x < 0:  # Moving left
                        self.hitbox.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:  # Moving down
                        self.hitbox.bottom = sprite.rect.top
                    elif self.direction.y < 0:  # Moving up
                        self.hitbox.top = sprite.rect.bottom
                
        
        self.rect.center = self.hitbox.center

    def take_hit_no_damage(self):
        pass
        #self.hit_sound_no_damage.play()

    def take_damage(self, damage):
        """This method is used to apply damage to the entity, ensuring it can only be damaged when vulnerable."""
        self.vulnerable = False # Set entity to invulnerable after being hit
        self.hit_sound.play()
        self.health -= damage  # Subtract health when hit
        #print (f'subtracting health, new health = {self}{self.health}')
        self.hit_time = pygame.time.get_ticks()  # Set the time of the hit
        if self.health <= 0: #check death
            self.death_sound.play()
            self.death_particles(self.rect.center, 'pop')
            destroy_sprite(self)

    def display_health(self):
        health_bar = pygame.Surface((self.health * 2, 10))
        self.health_rect = health_bar.get_rect(center = (self.rect.x, self.rect.y - 20))
        health_bar.fill((255, 0, 0))
       
        
    def death_particles(self,pos,particle_type):
        self.animation_player.create_particles(
            particle_type,
            pos,
            [self.dynamic_sprites],
            z=self.z,
        )

