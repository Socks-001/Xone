import pygame
from config import config
from enemy_data import enemy_data
from player_data import player_data
from entity import Entity
from debug import debug
from level_data import level
from projectile import Projectile
from weapon_data import weapons
import pathfinding


class Enemy(Entity):
    def __init__(self, name, pos, groups, sprite_type):
        
        # General Setup
        super().__init__(pos, groups, sprite_type, name)
        self.player = player_data['player']
        
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
        self.dynamic_sprites = level['sprite_groups']['dynamic_sprites']
        self.weapon_name = 'test'
        self.player_direction = None
        self.collision_tolerance = 5
        self.vulnerable = True
        self.status = 'hunt'
        
        # Cooldown Handling
        self.fire_rate = weapons[self.weapon_name]['fire_rate']  # Default 1000ms (1 sec) if not in data
        self.last_shot_time = 0  # Time when last shot was fired

        # A* Pathfinding
        self.pos = pos
        self.path = []
        self.path_index = 0
        self.grid = level['current']['pathfinding_grid']
     
    def get_target_distance_direction(self, target):
        target_location = pygame.math.Vector2(target.hitbox.center)
        self_location = pygame.math.Vector2(self.rect.center)

        # Calculate distance
        target_distance = (target_location - self_location).magnitude()

        # Always normalize the direction, even for small distances
        direction_vector = target_location - self_location
        if direction_vector.length() != 0:
            target_direction = direction_vector.normalize()
        else:
            target_direction = pygame.math.Vector2()

        return (target_distance, target_direction)
    
    def can_shoot(self):
        """Returns True if the enemy can shoot based on cooldown."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.fire_rate
    
    def follow_path_to_player(self, player):
        TILESIZE = config['screen']['TILESIZE']
        start = (int(self.rect.centerx // TILESIZE), int(self.rect.centery // TILESIZE))
        goal = (int(player.rect.centerx // TILESIZE), int(player.rect.centery // TILESIZE))
        
        # Always recalculate path each update for responsiveness
        self.path = pathfinding.astar(self.grid, start, goal)
        self.path_index = 0

        if self.path:
            next_tile = self.path[self.path_index]
            next_pos = pygame.math.Vector2((next_tile[0] * TILESIZE) + TILESIZE // 2,
                                        (next_tile[1] * TILESIZE) + TILESIZE // 2)
            direction_to_player = (next_pos - pygame.math.Vector2(self.rect.center)).normalize()
            self.direction = direction_to_player
            self.move(self.speed)

        # Optional: smooth follow
        if self.path_index < len(self.path) - 1:
            if pygame.math.Vector2(self.rect.center).distance_to(next_pos) < 4:
                self.path_index += 1
            else:
                self.direction = pygame.math.Vector2()  # Stop if at destination

        
    def enemy_behavior(self, player):
        """ Updates enemy status and behavior based on distance and action type. """
        distance_to_target, direction = self.get_target_distance_direction(player)
        
        if distance_to_target <= self.attack_radius and distance_to_target > 0:
            self.status = 'attack'
            self.shoot(direction)
        
        elif distance_to_target < 120:
            self.status = 'hunt'
            self.follow_path_to_player(player)
        
        else:
            self.status = 'idle'
            self.direction = pygame.math.Vector2()  # Stop moving

    def shoot(self, target_direction):
        """Fires a projectile if the cooldown allows it."""
        if self.can_shoot():

            if target_direction.length_squared() == 0:
                print(
                f"Skipping shot: enemy at {self.rect.center}, player at {self.player.rect.center}"
                )
                return

            Projectile(
                self,
                self.sprite_type,
                [self.visible_sprites, self.weapon_group, self.dynamic_sprites],
                target_direction,
                self.weapon_name,
            )
             
            self.last_shot_time = pygame.time.get_ticks()  # Update last shot time
    
    def update(self,):
        self.enemy_behavior(self.player)
        self.vulnerability_cooldown()
        
            
        