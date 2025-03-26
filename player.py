import pygame
from entity import Entity
from settings import config
from utilities import search_dict

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, controls):
        super().__init__(pos, groups, 'player', obstacle_sprites)
        self.speed = 0.15
        self.controls = controls
        self.menu_running = search_dict(config,'menu_running')
        print (f'Player coordinates = {self.hitbox.center}')

    def update(self):
        
        if not self.menu_running:
            self.direction = self.controls.direction
            self.shoot_direction = self.controls.shoot_direction
            self.move(self.speed)
            print (f'Player coordinates = {self.hitbox.center}')