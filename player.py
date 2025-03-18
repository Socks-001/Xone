import pygame
from entity import Entity
from controls import Controls

class Player(Entity):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(pos, groups, 'player', obstacle_sprites)
        self.speed = 5
        self.controls = Controls()

    def input(self):
        self.controls.input()
        self.direction = self.controls.direction

    def update(self):
        self.input()
        self.move(self.speed)
        #print(f'Player position: {self.rect.topleft}')