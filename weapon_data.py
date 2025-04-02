import pygame
pygame.init()

weapons = {
    'test': {'name' : 'test_weapon',
             'damage': 1,
             'sprite': None, 
             'speed': 2.5,
             'fire_rate': 300,
             'accuracy' :[0.98, 0.95] },
    'enemy_weapon': {'name' : 'enemy_weapon',
                    'damage': 1,
                    'sprite': None, 
                    'speed': 1.5,
                    'fire_rate': 1000,
                    'accuracy' : [1.00, 0.98]}
        }

def load_projectile_images():
    # Load Test sprite
    test_projectile = pygame.image.load('graphics/projectiles/test.png').convert_alpha()
    weapons['test']['sprite'] = test_projectile
    weapons['enemy_weapon']['sprite'] = test_projectile
    print (f" weapon = {weapons['test']['sprite']}")

