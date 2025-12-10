import pygame
from config import config

color_list = config['color_list']

shape_list = {
            'circle': pygame.draw.circle,
            'aacircle': pygame.draw.aacircle,
            'rect': pygame.draw.rect,
            'ellipse': pygame.draw.ellipse
        }

light_types = {
    '50': {
        'sprite_type': 'light',
        'type': 'torch',
        'shape': 'circle',
        'draw_shape': shape_list['circle'], 
        'radius': 16, 
        'color' : color_list['yellow'], 
        'flicker': True,
        'ebb': False},
        
    '51': {
        'sprite_type': 'light',
        'type': 'lamp',
        'shape': 'circle',
        'draw_shape': shape_list['circle'], 
        'radius': 32, 
        'color': color_list['off_white'], 
        'flicker': False,
        'ebb': True,
        'ebb_frequency': 0.5,},

    '52': {
        'sprite_type': 'light',
        'type': 'cursed',
        'shape': 'circle',
        'draw_shape': shape_list['circle'],  
        'radius': 8, 
        'color': color_list['purple'], 
        'flicker': True, 
        'ebb': False,
        'decay': 0.1},

    '53':{
        'sprite_type': 'light',
        'type': 'bullet_tracer',
        'shape': 'circle',
        'draw_shape': shape_list['circle'], 
        'radius': 24, 
        'color' : color_list['red'], 
        'flicker': False,
        'ebb': False},
}

