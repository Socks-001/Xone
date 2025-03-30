import pygame
pygame.init()

weapons = {
    'test': { 'name' : 'test_weapon',
              'sprite': None, 
              'speed': 1.5}
        }

def load_projectile_images():
    # Load Test sprite
    test_projectile = pygame.image.load('graphics/projectiles/test.png').convert_alpha()
    weapons['test']['sprite'] = test_projectile

