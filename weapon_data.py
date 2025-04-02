import pygame
pygame.init()

weapons = {
    'test': {'name' : 'test_weapon',
             'damage': 1,
             'sprite': None, 
             'speed': 1.5,
             'fire_rate': 1000}
        }

def load_projectile_images():
    # Load Test sprite
    test_projectile = pygame.image.load('graphics/projectiles/test.png').convert_alpha()
    weapons['test']['sprite'] = test_projectile
    print (f" weapon = {weapons['test']['sprite']}")

