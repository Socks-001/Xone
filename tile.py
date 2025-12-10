import pygame
from config import config
from utilities import search_dict

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface):
        super().__init__(groups)

        self.sprite_type = sprite_type

        self.image = surface

        # Base slice size (e.g., 16 if your sheet is 16xN)
        d = self.stack_slice_len(self.image)

        # Build rect/hitbox as a square (d, d)
        self.rect = pygame.Rect(0,0,d,d)
        self.rect.center = pos
        self.hitbox = pygame.FRect(self.rect)

        # Place by topleft or center to match your world semantics
        '''if pos_is_center:
            self.rect.center = pos
            self.hitbox.center = pos
        else:
            self.rect.topleft = pos
            self.hitbox.topleft = pos
        '''
    @staticmethod
    def stack_slice_len(surface: pygame.Surface) -> int:
        """Square base size (px) assumed by stacked sheets (min of w/h)."""
        return min(surface.get_width(), surface.get_height())
