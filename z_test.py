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
        w = max(1, target.rect.width)
        self.base_radius = max(4, w // 4)
        self._cache = {}
        self.image = self._get_blob(self.base_radius)
        self.rect = self.image.get_rect(center=target.rect.center)
        self.hitbox = pygame.FRect(self.rect)
        self.z = -1.0
        self.z_height = config['render']['Z_UNIT']
        self._moved = True

    def _get_blob(self, radius):
        blob = self._cache.get(radius)
        if blob is None:
            size = radius * 2
            blob = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.ellipse(blob, (0, 0, 0, 110), blob.get_rect())
            self._cache[radius] = blob
        return blob

    def update(self, dt=0.0):
        z = getattr(self.target, "z", 0.0)
        max_z = getattr(self.target, "z_max", config['render']['Z_UNIT'])
        if max_z > 0:
            t = max(0.0, min(1.0, z / max_z))
        else:
            t = 0.0
        scale = max(0.3, 1.0 - t * 0.7)
        radius = max(2, int(round(self.base_radius * scale)))
        self.image = self._get_blob(radius)
        center = self.target.hitbox.center
        self.rect = self.image.get_rect(center=center)
        self.hitbox = pygame.FRect(self.rect)
        self._moved = True
