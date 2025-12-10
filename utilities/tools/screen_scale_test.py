import pygame
import sys

# Settings
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240
FPS = 60
TILESIZE = 16
BG_COLOR = (0, 0, 0)
SCALE_FACTORS = [1, 2, 4, 6]  # Predefined scaling options

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        try:
            self.image = pygame.image.load("graphics/level/29.png").convert_alpha()
        except pygame.error:
            print("Failed to load image, using fallback color")
            self.image = pygame.Surface((TILESIZE, TILESIZE))
            self.image.fill((0, 255, 0))  # Fallback to green square
        self.FRect = self.image.get_frect(topleft=pos)

def trigger_resize_event(current_index):
    """Trigger a VIDEORESIZE event with the next scale factor in the list."""
    new_index = (current_index + 1) % len(SCALE_FACTORS)
    new_scale = SCALE_FACTORS[new_index]
    new_width = SCREEN_WIDTH * new_scale
    new_height = SCREEN_HEIGHT * new_scale
    pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE, w=new_width, h=new_height))
    return new_index  # Return the updated index

def main():
    pygame.init()
    
    scale_factor_index = 0  # Track which scale factor we're using
    scale_factor = SCALE_FACTORS[scale_factor_index]

    screen = pygame.display.set_mode((SCREEN_WIDTH * scale_factor, SCREEN_HEIGHT * scale_factor), pygame.RESIZABLE)
    pygame.display.set_caption("Scaling Display Test")
    clock = pygame.time.Clock()

    # Create player
    player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    all_sprites = pygame.sprite.Group(player)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                scale_factor_index = trigger_resize_event(scale_factor_index)
            elif event.type == pygame.VIDEORESIZE:
                scale_factor = event.w // SCREEN_WIDTH
                screen = pygame.display.set_mode((SCREEN_WIDTH * scale_factor, SCREEN_HEIGHT * scale_factor), pygame.RESIZABLE)

        # Create a surface to render the game
        game_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        game_surface.fill(BG_COLOR)
        all_sprites.draw(game_surface)

        # Scale the game surface to fit the screen
        scaled_surface = pygame.transform.scale(game_surface, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
