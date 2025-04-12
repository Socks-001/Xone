import pprint
import pygame
from graphics_data import graphics
from utilities import search_dict

enemy_data = {   
    'goblin': {
        'enemy_type': 'crasher',
        'attack_radius': 60,
        'attack_sound': None,
        'attack_type': 'contact',
        'damage': 5,
        'exp': 10,
        'health': 2,
        'notice_radius': 100,
        'resistance': 10,
        'speed': 1.5,
        'sprite': graphics['enemies']['goblin']}             
    	}

def load_enemy_images():
    for enemy_name in enemy_data:
        sprite = search_dict(graphics, enemy_name)
        if sprite:
            enemy_data[enemy_name]['sprite'] = sprite
        else:
            print(f"⚠️ Sprite not found for enemy '{enemy_name}' in graphics.")