import pygame
from config import config
from utilities import search_dict

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((search_dict(config,'TILESIZE'),search_dict(config,'TILESIZE')))):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.FRect(self.rect.inflate(0, -10))
    