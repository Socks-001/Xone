import pygame
from weapon_data import weapons
from level_data import level
from settings import config 

pygame.init()

class Weapon(pygame.sprite.Sprite):
    def __init__(self, owner, owner_sprite_type, groups, shoot_direction, weapon_name):
        super().__init__(groups)	

        self.owner = owner
        self.owner_sprite_type = owner_sprite_type # differentiates player/enemy
        self.direction = shoot_direction.normalize() # direction to shoot
        self.SCREEN_WIDTH = config['screen']['SCREEN_WIDTH']

        # Weapon Data (Dynamic)
        weapon_data = weapons[weapon_name]
        self.sprite_type = weapon_data['sprite']
        self.attack_damage = weapon_data['damage']
        self.sprite = weapon_data['sprite']
        self.velocity = float(weapon_data['speed']) # Speed projectile travles at 
        self.cooldown = weapon_data['fire_rate'] # cooldown between shots
        self.lifetime = pygame.time.get_ticks()

        # Image and Rect 
        self.image = self.sprite  # Load sprite
        self.projectile_rect = self.image.get_rect()
        self.projectile_hitbox = pygame.FRect(self.projectile_rect)

        # Obstacle and Entity reference 
        self.obstacle_sprites = level['sprite_groups']['obstacle_sprites']
        self.entity_sprites = level['sprite_groups']['entity_sprites']

    def move_projectile(self, velocity):

        self.projectile_hitbox += ((self.direction.x * velocity), (self.direction.y * velocity))
        self.projectile_rect.center = self.projectile_hitbox.center

    def lifetime_check(self):
        if pygame.time.get_ticks() - self.lifetime > 1000:  # 1 second, lifetime of projectile
            self.kill()

    def check_collision(self):
        # check collisions with entities 
        for entity in self.entity_sprites:
            if self.projectile_hitbox.colliderect(entity.hitbox):
                # Check if the entity is of a different sprite type (not the owner)
                if entity.sprite_type != self.owner_sprite_type:
                    if entity.vulnerable:
                        entity.take_damage(self.attack_damage)  # Apply damage
                        entity.vulnerable = False  # Entity becomes invulnerable after being hit
                        self.kill()  # Destroy the projectile
                  
                elif entity.vulnerable == False:
                    self.kill()

                else:
                    pass
        # check collisions with obstacles                
        for sprite in self.obstacle_sprites:
            if self.projectile_hitbox.colliderect(sprite.rect) or self.projectile_hitbox.x > + self.SCREEN_WIDTH + 4 or self.projectile_hitbox.x <= 0:
                self.kill()
        

    def update(self):
        
        self.check_collision()
        self.move_projectile(self.velocity)
        self.lifetime_check()

        #Treasure of the Rudras SNES Art
        #Shadownrun SNES