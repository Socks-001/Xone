import pygame

class Light(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, radius):
        super().__init__(groups)

        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.aacircle(self.image, (255, 255, 100, 180), (radius, radius), radius)
        self.rect = self.image.get_rect(topleft = pos)