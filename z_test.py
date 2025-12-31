import pygame
from config import config
from level_data import level


class ZBounceTest(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, z_min=0.0, z_max=64.0, z_vel=8.0, gravity_scale=1.0, shadow_surface=None):
        super().__init__(groups)
        self.sprite_type = 'z_test'
        self.image = surface
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = pygame.FRect(self.rect)
        self.z = 0.0
        self.z_height = config['render']['Z_UNIT']
        self.z_vel = z_vel
        self.z_min = z_min
        self.z_max = z_max
        self.gravity_scale = gravity_scale
        self._moved = True
        self.shadow = None
        if shadow_surface is not None:
            self.shadow = ZTestShadow(self, shadow_surface)
            level['sprite_groups']['dynamic_sprites'].add(self.shadow)

    def update(self, dt=0.0):
        dt_scale = dt * config['screen']['LOGIC_FPS']
        g = config['physics']['gravity'] * self.gravity_scale
        if g != 0.0:
            self.z_vel -= g * dt_scale
        self.z += self.z_vel * dt_scale

        if self.z < self.z_min:
            self.z = self.z_min
            self.z_vel = abs(self.z_vel)
        elif self.z > self.z_max:
            self.z = self.z_max
            self.z_vel = -abs(self.z_vel)


class ZTestShadow(pygame.sprite.Sprite):
    def __init__(self, target, surface):
        super().__init__()
        self.sprite_type = 'z_test_shadow'
        self.target = target
        self.base_image = surface.copy()
        self.base_image.fill((0, 0, 0, 140), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = surface
        self.rect = self.image.get_rect(center=target.rect.center)
        self.hitbox = pygame.FRect(self.rect)
        self.z = -1.0
        self.z_height = config['render']['Z_UNIT']
        self._moved = True

    def update(self, dt=0.0):
        z = getattr(self.target, "z", 0.0)
        max_z = getattr(self.target, "z_max", config['render']['Z_UNIT'])
        if max_z > 0:
            t = max(0.0, min(1.0, z / max_z))
        else:
            t = 0.0
        scale = max(1, int(round(1 + (1.0 - t) * 2)))
        self.image = pygame.transform.scale(
            self.base_image,
            (self.base_image.get_width() * scale, self.base_image.get_height() * scale),
        )
        center = self.target.hitbox.center
        self.rect = self.image.get_rect(center=center)
        self.hitbox = pygame.FRect(self.rect)
        self._moved = True
