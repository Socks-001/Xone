import pygame
from entity import Entity
from settings import config

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(pos, groups, 'player', obstacle_sprites)
        self.speed = 5.0
        self.controls = config['controls']['controls']
        self.menu_running = config['menu']['menu_running']
        print (f'Player coordinates = {self.hitbox.center}')

    def update(self):
        
        if not self.menu_running:
            self.direction = self.controls.direction
            self.shoot_direction = self.controls.shoot_direction
            self.move(self.speed)
            print (f'Player coordinates = {self.hitbox.center}')