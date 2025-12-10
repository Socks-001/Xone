import pygame
from graphics_data import load_graphics
from player_data import load_player_images
from enemy_data import load_enemy_images
from weapon_data import load_projectile_images, load_projectile_sfx
from sfx import load_sfx
from config import config, load_menu_sfx
from level_data import load_level_data 
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
    

    # Update Config
    config['screen']['screen'] = screen
    config['screen']['game_surface'] = game_surface

    # Load Graphics Assetssd
    print("Loading assets...")    
    load_graphics()
    load_player_images()
    load_enemy_images()
    load_projectile_images()
    load_level_data()

    # Load SFX Assets 
    load_sfx()
    load_projectile_sfx()
    load_menu_sfx()


    return screen, game_surface

if __name__ == '__main__':
    # Initialize resources
    
    screen, game_surface = initialize()

    # Run the game loop
    game_engine = GameEngine(screen, game_surface)
    game_engine.run()
