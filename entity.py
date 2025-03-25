import pygame
from settings import config
from utilities import search_dict

class Entity(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = sprite_type
        tile_size = search_dict(config, 'TILESIZE') 
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.FRect(self.rect.inflate(0, -10))
        self.direction = pygame.math.Vector2()
        self.obstacle_sprites = obstacle_sprites
        self.vulnerable = True
        self.health = 100
        self.collision_tolerance = 10

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        #self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        #self.collision('vertical')
        self.rect.center = self.hitbox.center

        #Treasure of the Rudras SNES Art
        #Shadownrun SNES