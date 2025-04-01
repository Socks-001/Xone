import pygame
from enemy_data import enemy_data
from entity import Entity
from debug import debug
from level_data import level
from weapon import Weapon


class Enemy(Entity):
    def __init__(self, name, pos, groups, player, sprite_type):
        # general setup
        super().__init__(pos, groups, sprite_type, name)
        self.player = player
        
        # stats
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

        self.weapon_group = level['sprite_groups']['weapons_sprites']
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.weapon_name = 'test'
        self.player_direction = None
        self.collision_tolerance = 5
        self.vulnerable = True
        self.status = 'Idle'
     
    def get_target_distance_direction(self, target):
        target_location = pygame.math.Vector2(target.hitbox.center)
        self_location = pygame.math.Vector2(self.rect.center)

        # Calculate distance
        distance = (target_location - self_location).magnitude()

        # Always normalize the direction, even for small distances
        direction = (target_location - self_location).normalize()
        return (distance, direction)
        
    def enemy_behavior(self, player):
        """ Updates enemy status and behavior based on distance and action type. """
        distance, direction = self.get_target_distance_direction(player)
        
        if distance <= self.attack_radius:
            self.status = 'attack'
            self.shoot(direction)
            
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.rect.center += direction * self.speed  # Move toward player
           
    def shoot(self, player_direction):
            Weapon(self, self.sprite_type, [self.visible_sprites, self.weapon_group], player_direction, self.weapon_name)
    
    def update(self,):
        self.enemy_behavior(self.player)
        
            
        