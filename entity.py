import pygame
from config import config
from level_data import level
from player_data import player_data
from enemy_data import enemy_data

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
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.FRect(self.rect.inflate(-self.collision_tolerance, -self.collision_tolerance))
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        
    
      # Vulnerability properties
        self.vulnerable = True  # Entity is initially vulnerable
        self.hit_time = 0  # Time when the entity was last hit
        self.invulnerability_duration = 500  # Time in milliseconds (e.g., 500ms = 0.5 seconds)

    def vulnerability_cooldown(self):
        """Handles the cooldown for vulnerability."""
        if not self.vulnerable:
            if pygame.time.get_ticks() - self.hit_time > self.invulnerability_duration:
                self.vulnerable = True  # Entity becomes vulnerable again after the cooldown period

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # Horizontal movement and collision check
        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')

        # Vertical movement and collision check
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')

        # Update rect position after movement
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        """Handles collision detection and prevents movement through obstacles."""
        for sprite in self.obstacle_sprites:
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

    def take_damage(self, damage):
        """This method is used to apply damage to the entity, ensuring it can only be damaged when vulnerable."""
        if self.vulnerable:
            self.health -= damage  # Subtract health when hit
            print (f'subtracting health, new health = {self.health}')
            self.vulnerable = False  # Set entity to invulnerable after being hit
            self.hit_time = pygame.time.get_ticks()  # Set the time of the hit
            if self.health <= 0:
                self.kill()
        
    '''def death_particles(self,pos,particle_type):
        self.animation_player.create_particles(particle_type,pos,self.weapon_sprites)'''

