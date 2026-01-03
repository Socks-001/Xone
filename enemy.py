import math
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
from utilities import z_ranges_overlap


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
        self.repath_interval = 0.3
        self.repath_timer = 0.0
        self.last_goal_tile = None
        self.last_known_pos = None
        self.facing_dir = pygame.math.Vector2(0, 1)
        self.vision_range = self.notice_radius * config['screen']['TILESIZE']
        self.vision_base_radius = enemy_info.get('vision_base_diameter', 16) * 0.5
        self.vision_min_range = config['ai']['VISION_MIN_RANGE']
     
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

    def _update_facing(self, direction):
        if direction.length_squared() > 0:
            self.facing_dir = direction.normalize()

    def can_see_target(self, target):
        if not z_ranges_overlap(self, target):
            return False

        origin = pygame.math.Vector2(self.hitbox.center)
        to_target = pygame.math.Vector2(target.hitbox.center) - origin
        distance = to_target.length()
        if distance == 0:
            return True
        if distance > self.vision_range:
            return False

        vision_range = max(self.vision_min_range, self.vision_range)
        half_angle = math.atan2(self.vision_base_radius, vision_range)
        dir_norm = to_target / distance
        face = self.facing_dir
        if face.length_squared() == 0:
            face = dir_norm
        else:
            face = face.normalize()
        return face.dot(dir_norm) >= math.cos(half_angle)

    def follow_path_to_target(self, target_pos, dt):
        TILESIZE = config['screen']['TILESIZE']
        start = (int(self.rect.centerx // TILESIZE), int(self.rect.centery // TILESIZE))
        goal = (int(target_pos[0] // TILESIZE), int(target_pos[1] // TILESIZE))
        
        self.repath_timer += dt
        if self.last_goal_tile is None:
            self.last_goal_tile = goal

        if self.repath_timer >= self.repath_interval or goal != self.last_goal_tile or not self.path:
            self.path = pathfinding.astar(self.grid, start, goal)
            self.path_index = 0
            self.repath_timer = 0.0
            self.last_goal_tile = goal

        if not self.path:
            self.direction = pygame.math.Vector2()
            return

        next_tile = self.path[self.path_index]
        next_pos = pygame.math.Vector2((next_tile[0] * TILESIZE) + TILESIZE // 2,
                                    (next_tile[1] * TILESIZE) + TILESIZE // 2)
        direction_vec = (next_pos - pygame.math.Vector2(self.rect.center))
        if direction_vec.length_squared() == 0:
            self.direction = pygame.math.Vector2()
        else:
            self.direction = direction_vec.normalize()
        self._update_facing(self.direction)
        dt_scale = dt * config['screen']['LOGIC_FPS']
        self.move(self.speed * dt_scale)

        # Optional: smooth follow
        if self.path_index < len(self.path) - 1:
            if pygame.math.Vector2(self.rect.center).distance_to(next_pos) < 4:
                self.path_index += 1
            else:
                self.direction = pygame.math.Vector2()  # Stop if at destination

        
    def enemy_behavior(self, player, dt):
        """ Updates enemy status and behavior based on distance and action type. """
        distance_to_target, direction = self.get_target_distance_direction(player)
        can_see = self.can_see_target(player)
        
        if can_see:
            self.last_known_pos = pygame.math.Vector2(player.hitbox.center)
            self._update_facing(direction)

        if can_see and distance_to_target <= self.attack_radius and distance_to_target > 0:
            self.status = 'attack'
            self.shoot(direction)
        
        elif can_see and distance_to_target < self.vision_range:
            self.status = 'hunt'
            self.follow_path_to_target(player.hitbox.center, dt)
        
        elif self.last_known_pos is not None:
            self.status = 'search'
            self.follow_path_to_target(self.last_known_pos, dt)
            if pygame.math.Vector2(self.rect.center).distance_to(self.last_known_pos) < 8:
                self.last_known_pos = None
                self.path = []
                self.direction = pygame.math.Vector2()

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
    
    def update(self, dt=0.0):
        self.enemy_behavior(self.player, dt)
        dt_scale = dt * config['screen']['LOGIC_FPS']
        self.apply_gravity(dt_scale)
        self.vulnerability_cooldown()
        
            
        
