import pygame
from graphics_data import graphics
player_data = { 'player' : None,
                'speed' : 1.5,
                'health' : 4, 
                'sprite' : None
}

def load_player_images():
    # Load Test sprite
    player_sprite = graphics['player']['sprite']
    player_data['sprite'] = player_sprite