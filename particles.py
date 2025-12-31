import pygame
from config import config
from graphics_data import graphics
from utilities import destroy_sprite

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'pop': graphics['particles']['pop'],
        }

    def create_particles(self, animation_type, pos, groups, z=0.0):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups, z=z)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, z=0.0, velocity=None, gravity_scale=1.0):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.FRect(self.rect)
        self.z = z
        self.z_height = config['render']['Z_UNIT']
        self.velocity = pygame.math.Vector2(velocity) if velocity is not None else pygame.math.Vector2()
        self.gravity_scale = gravity_scale
        self._moved = True

    def animate(self, dt):
        dt_scale = dt * config['screen']['LOGIC_FPS']
        self.frame_index += self.animation_speed * dt_scale
        if self.frame_index >= len(self.frames):
            destroy_sprite(self)
        else:
            center = self.rect.center
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=center)
            self.hitbox.center = self.rect.center

    def update(self, dt=0.0):
        dt_scale = dt * config['screen']['LOGIC_FPS']
        prev_center = self.hitbox.center
        if config['physics']['gravity'] != 0.0 and self.gravity_scale != 0.0:
            self.velocity.y += config['physics']['gravity'] * self.gravity_scale * dt_scale
        if self.velocity.length_squared() != 0:
            self.hitbox.x += self.velocity.x * dt_scale
            self.hitbox.y += self.velocity.y * dt_scale
            self.rect.center = self.hitbox.center
        moved = (self.hitbox.center != prev_center)
        self._moved = self._moved or moved
        self.animate(dt)
