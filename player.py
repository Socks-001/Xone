import pygame
from entity import Entity
from settings import config
from weapon_data import weapons
from weapon import Weapon
from player_data import player_data
from level_data import level

class Player(Entity):
    def __init__(self, pos, groups, controls):
        super().__init__(pos, groups, 'player')
        self.speed = player_data['speed']
        self.health = player_data['health']
        self.controls = controls
        self.menu_running = config['menu']['menu_running'] #??
        self.weapon_group = level['sprite_groups']['weapons_sprites']
        self.visible_sprites = level['sprite_groups']['visible_sprites']
        self.weapon_name = 'test'
        
    def shoot(self):
        """Creates a projectile if shoot_direction is outside the deadzone."""
        if self.controls.shoot_direction.length() > 0.2:  # Adjust 0.2 as needed for deadzone
            Weapon(self, self.sprite_type, [self.visible_sprites, self.weapon_group], self.controls.shoot_direction, self.weapon_name)
            print('shot')
    

    def update(self):
        if not self.menu_running:
            self.direction = self.controls.direction #??
            self.shoot()  # Call shoot method
            self.move(self.speed)
            self.vulnerability_cooldown()
            #print (f'pos = {self.hitbox.center}')