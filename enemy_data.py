import pprint
import pygame
pygame.init()

enemy_data = {   
    'test': {   'enemy_type': 'crasher',
                      'attack_radius': 60,
                      'attack_sound': None,
                      'attack_type': 'contact',
                      'damage': 5,
                      'exp': 10,
                      'health': 2,
                      'notice_radius': 100,
                      'resistance': 10,
                      'speed': 1.5},
                      'sprite': None             
    	}

def load_enemy_images():
    # Load Test sprite
    enemy_sprite = pygame.image.load('graphics/enemies/test.png').convert_alpha()
    enemy_data['test']['sprite'] = enemy_sprite
    