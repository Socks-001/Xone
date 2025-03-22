import pygame
from entity import Entity

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites, controls, menu):
        super().__init__(pos, groups, 'player', obstacle_sprites)
        self.speed = 5
        self.controls = controls
        self.menu = menu
        self.pos = pos
        print (f'Player coordinates = {self.pos}')

    def update(self):
        if not self.menu.running:
            self.direction = self.controls.direction
            self.shoot_direction = self.controls.shoot_direction
            self.move(self.speed)
            print (f'Player coordinates = {self.pos}')
        #print(f'Player position: {self.rect.topleft}')
