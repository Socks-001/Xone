import pygame
from enemy_data import enemy_data
from entity import Entity
from debug import debug


class Enemy(Entity):
    def __init__(self, name, pos, groups, player, sprite_type):
        # general setup
        super().__init__(pos, groups, player, sprite_type)
        self.player = player
        
        # stats
        self.health = enemy_data[name]['health'] 
        self.exp = enemy_data[name]['exp'] 
        self.attack_type = enemy_data[name]['attack_type'] 
        self.attack_sound = enemy_data[name]['attack_sound'] 
        self.damage = enemy_data[name]['damage'] 
        self.speed = enemy_data[name]['speed']
        self.resistance = enemy_data[name]['resistance'] 
        self.attack_radius = enemy_data[name]['attack_radius'] 
        self.notice_radius = enemy_data[name]['notice_radius']
        self.enemy_type = enemy_data[name]['enemy_type']
        self.weapon_name = 'test'

        # graphics
        self.import_graphics(name)
        self.status = 'idle' # initializing default state
        self.image = self.animations[self.status][int(self.frame_index)]
        self.collision_tolerance = 5
    

        # player interaction
        self.can_attack = True
        self.attack_time = pygame.time.get_ticks()
        self.attack_cooldown = 2000
        self.hit_time = None
        self.vulnerable = True
        self.invincibility_duration = 100

    def get_target_distance_direction(self, object):
        object_vec = pygame.math.Vector2 (object.center)
        enemy_vec = pygame.math.Vector2 (self.rect.center)

        distance = (object_vec - enemy_vec).magnitude()

        if distance > 0.8:
            direction = (object_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)

    def enemy_behavior(self, player):
        """ Updates enemy status and behavior based on distance and action type. """
        distance, direction = self.get_target_distance_direction(player)

        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_cooldown:
            self.can_attack = True
        
        if distance <= self.attack_radius and self.can_attack:
            self.status = 'attack'
            self.attack(player)
            self.attack_time = pygame.time.get_ticks()
            self.can_attack = False
           
        elif distance <= self.notice_radius:
            self.status = 'move'
            self.direction = direction  # Move towards the player
        else:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()  # Default movement