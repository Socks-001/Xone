import pygame
from config import config
from level_data import load_level_data
from weapon_data import load_projectile_images
from player_data import load_player_images
from enemy_data import load_enemy_images
from game_engine import GameEngine  # Import the game loop logic
from utilities import init_audio

def initialize():
    """Initialize Pygame, screen, and load assets."""
    print("Initializing Pygame...")
    pygame.init()
    init_audio()

    # Screen and Surface Setup
    screen_width = config['screen']['SCREEN_WIDTH']
    screen_height = config['screen']['SCREEN_HEIGHT']
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED)
    game_surface = pygame.Surface((screen_width, screen_height))
    scaled_surface = pygame.transform.scale(game_surface, (screen_width, screen_height))

    # Update Config
    config['screen']['screen'] = screen
    config['screen']['game_surface'] = game_surface
    config['screen']['scaled_surface'] = scaled_surface

    # Load Assets
    print("Loading assets...")
    load_level_data()
    load_projectile_images()
    load_player_images() 
    load_enemy_images()
    print("Assets loaded successfully.")
    
    return screen, game_surface, scaled_surface

if __name__ == '__main__':
    # Initialize resources
    screen, game_surface, scaled_surface = initialize()

    # Run the game loop
    game_engine = GameEngine(screen, game_surface, scaled_surface)
    game_engine.run()
