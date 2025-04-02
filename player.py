import pygame
from entity import Entity
from settings import config
from weapon_data import weapons
from weapon import Weapon
from player_data import player_data
from level_data import level

class Player(Entity):
    def __init__(self, pos, groups, controls):
        super().__init__(pos, groups, 'player', 'player')
        self.speed = player_data['speed']
        self.health = player_data['health']
        self.controls = controls
        self.menu_running = config['menu']['menu_running'] #??
        self.weapon_group = level['sprite_groups']['weapons_sprites']
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.weapon_name = 'test'
    
         # Cooldown Handling
        self.fire_rate = weapons[self.weapon_name]['fire_rate']  # Get cooldown from weapon data
        self.last_shot_time = 0  # Time when last shot was fired

    def can_shoot(self):
        """Returns True if the player can shoot based on cooldown."""
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.fire_rate
        
    def shoot(self):
        """Creates a projectile if shoot_direction is outside the deadzone."""
        if self.controls.shoot_direction.length() > 0.2 and self.can_shoot():  # Adjust 0.2 as needed for deadzone
            Weapon(self, self.sprite_type, [self.visible_sprites, self.weapon_group], self.controls.shoot_direction, self.weapon_name)
            self.last_shot_time = pygame.time.get_ticks()
    

    def update(self):
        if not self.menu_running:
            self.direction = self.controls.direction #??
            self.shoot()  # Call shoot method
            self.move(self.speed)
            self.vulnerability_cooldown()
            #print (f'pos = {self.hitbox.center}')