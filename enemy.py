import pygame
from enemy_data import enemy_data
from entity import Entity
from debug import debug
from level_data import level
from weapon import Weapon
from weapon_data import weapons


class Enemy(Entity):
    def __init__(self, name, pos, groups, player, sprite_type):
        
        # General Setup
        super().__init__(pos, groups, sprite_type, name)
        self.player = player
        
        # Stats
        enemy_info = enemy_data[name]  # Store dictionary reference for cleaner code
        self.health = enemy_info['health']
        self.exp = enemy_info['exp']
        self.attack_type = enemy_info['attack_type']
        self.attack_sound = enemy_info['attack_sound']
        self.damage = enemy_info['damage']
        self.speed = enemy_info['speed']
        self.resistance = enemy_info['resistance']
        self.attack_radius = enemy_info['attack_radius']
        self.notice_radius = enemy_info['notice_radius']
        self.enemy_type = enemy_info['enemy_type']
        self.sprite = enemy_info['sprite']

        #Weapon and Shooting
        self.weapon_group = level['sprite_groups']['weapons_sprites']
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.weapon_name = 'test'
        self.player_direction = None
        self.collision_tolerance = 5
        self.vulnerable = True
        self.status = 'Idle'
        
        # Cooldown Handling
        self.fire_rate = weapons[self.weapon_name]['fire_rate']  # Default 1000ms (1 sec) if not in data
        self.last_shot_time = 0  # Time when last shot was fired
     
    def get_target_distance_direction(self, target):
        target_location = pygame.math.Vector2(target.hitbox.center)
        self_location = pygame.math.Vector2(self.rect.center)

        # Calculate distance
        distance = (target_location - self_location).magnitude()

        # Always normalize the direction, even for small distances
        direction = (target_location - self_location).normalize()
        return (distance, direction)
    
    def can_shoot(self):
        """Returns True if the enemy can shoot based on cooldown."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.fire_rate
        
    def enemy_behavior(self, player):
        """ Updates enemy status and behavior based on distance and action type. """
        distance, direction = self.get_target_distance_direction(player)
        
        if distance <= self.attack_radius:
            self.status = 'attack'
            self.shoot(direction)
            
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.move(self.speed) # Move toward player
        
    def shoot(self, player_direction):
        """Fires a projectile if the cooldown allows it."""
        if self.can_shoot():
            Weapon(self, self.sprite_type, [self.visible_sprites, self.weapon_group], player_direction, self.weapon_name)
            self.last_shot_time = pygame.time.get_ticks()  # Update last shot time
    
    def update(self,):
        self.enemy_behavior(self.player)
        self.vulnerability_cooldown()
        
            
        