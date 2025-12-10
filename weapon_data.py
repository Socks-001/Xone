import pygame
from graphics_data import graphics
from sfx import sfx

weapons = {
    'test': {'name' : 'test_weapon',
             'damage': 1,
             'sprite': None,
             'shot_sound': None,
             'speed': 5,
             'fire_rate': 200,
             'ammo poermagazine' : 15,
             'total magazine' : 3,
             'current ammo' : 0,
             'accuracy' : 0.1,},
    'enemy_weapon': {'name' : 'enemy_weapon',
                    'damage': 1,
                    'sprite': None, 
                    'speed': 2.5,
                    'fire_rate': 200,
                    'accuracy' : [1.00, 0.98]}
        }

def load_projectile_images():
    # Load Test sprite
    weapons['test']['sprite'] = graphics['projectiles']['test']
    weapons['enemy_weapon']['sprite'] = graphics['projectiles']['test']

def load_projectile_sfx():
    sfx['weapon']['shot']
    


