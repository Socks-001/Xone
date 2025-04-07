import pygame
pygame.init()

player_data = { 'speed' : 1.5,
                'health' : 4, 
                'sprite' : None 
}

def load_player_images():
    # Load Test sprite
    player_sprite = pygame.image.load('graphics/player/test.png').convert_alpha()
    player_data['sprite'] = player_sprite