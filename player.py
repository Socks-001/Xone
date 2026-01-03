import pygame
from entity import Entity
from config import config
from weapon_data import weapons
from projectile import Projectile
from player_data import player_data
from level_data import level

class Player(Entity):
    def __init__(self, pos, groups, controls):
        super().__init__(pos, groups, 'player', 'player')
        self.speed = player_data['speed']
        self.health = player_data['health']
        self.controls = controls
        self.weapon_group = level['sprite_groups']['weapons_sprites']
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.dynamic_sprites = level['sprite_groups']['dynamic_sprites']
        self.weapon_name = 'test'
    
         # Cooldown Handling
        self.fire_rate = weapons[self.weapon_name]['fire_rate']  # Get cooldown from weapon data
        self.last_shot_time = 0  # Time when last shot was fired

    # --- aim direction
    def _aim_dir(self) -> pygame.Vector2:
        ax, ay = config['controls']['aim_vec']
        v = pygame.Vector2(ax, ay)
        # If right stick is active, you may already be feeding shoot_direction;
        # but aim_vec is now the single source of truth, so just use it:
        return v if v.length_squared() > 0 else pygame.Vector2(0, 1)



    def can_shoot(self):
        """Returns True if the player can shoot based on cooldown."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.fire_rate
        
    # --- replace your shoot() with this ---
    def shoot(self):
        if not config['controls']['fire_down']:
            return
        if not self.can_shoot():
            return

        dir_vec = self._aim_dir()
        Projectile(
            self,
            self.sprite_type,
            [self.visible_sprites, self.weapon_group, self.dynamic_sprites],
            dir_vec,
            self.weapon_name
        )
        self.last_shot_time = pygame.time.get_ticks()

        

    def update(self, dt=0.0):
        if not config['menu']['menu_running']:
            self.direction = self.controls.direction #??
            self.shoot()  # Call shoot method
            dt_scale = dt * config['screen']['LOGIC_FPS']
            self.move(self.speed * dt_scale)
            self.update_jump(dt_scale)
            self.vulnerability_cooldown()
            #print (f'pos = {self.hitbox.center}')

    def update_jump(self, dt_scale):
        ground_z = self.get_ground_z()
        if config['controls']['jump_pressed_once'] and ground_z is not None and self.z <= ground_z:
            self.z_vel = player_data['jump_velocity']

        self.apply_gravity(dt_scale, ground_z)
