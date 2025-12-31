import pygame
from graphics_data import graphics
from utilities import destroy_sprite

class AnimationPlayer:
    def __init__(self):
        self.frames = {
            'pop': graphics['particles']['pop'],
        }

    def create_particles(self,animation_type,pos,groups):
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos,animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self,pos,animation_frames,groups):
        super().__init__(groups)
        self.sprite_type = 'magic'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.FRect(self.rect)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            destroy_sprite(self)
        else:
            center = self.rect.center
            self.image = self.frames[int(self.frame_index)]
            self.rect = self.image.get_rect(center=center)
            self.hitbox.center = self.rect.center

    def update(self):
        self.animate()
