import pygame
from entity import Entity
from settings import config
from weapon_data import weapons

class Player(Entity):
    def __init__(self, pos, groups, controls):
        super().__init__(pos, groups, 'player')
        self.speed = 5.0
        self.controls = controls
        self.menu_running = config['menu']['menu_running']
        print (f'Player coordinates = {self.hitbox.center}')
        print(f"Entity initialized: {self}, Image: {self.image}, Rect: {self.rect}")

    def update(self):
        
        if not self.menu_running:
            self.direction = self.controls.direction
            self.shoot_direction = self.controls.shoot_direction
            self.move(self.speed)
            print (f'Player coordinates = {self.hitbox.center}')