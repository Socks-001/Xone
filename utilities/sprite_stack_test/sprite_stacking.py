import pygame
import math
import os
import sys
import numpy as np

# This is a test by Forgotten Druid to test the sprite stack and rotation in python 3 and pygame-ce 
# there is an issue that arises when rotation where a jitter occurs when the sprite is rotated
# this is due to a combination of squares creating longer dimensions on diagonals and the surface cropping to this new dimension
# that way the previous frame (surface size) is not the same as the current frame (surface size), and the image isnt "centered" on the screen
# Ultimately the problem is resolved by rotating the image and then applying it to a larger surface, which is then blitted to the screen
# I'm sure this can be improved upon and there are hard coded values but this is more a demonstration of the concept than a final product
# when you run the file there will be three image the first is the stacked sprite, the second is that same stack rotated, and the third is the same stack rotated but blitted to a larger surface
# you can cycle through available sprites by pressing the "a" and "d" keys

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

pygame.init()

class screen_setup:
    screen_size = 256
    screen = pygame.display.set_mode((screen_size, screen_size), pygame.SCALED)
    pygame.display.set_caption("Sprite Stack Test")


class SpriteStackTest:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.debug_slice = 0  # Start with full stack display
        self.debug_enabled = False
        self.input_cooldown = 20  # Cooldown in milliseconds
        self.last_input_time = 0  # Tracks the last time an input was processed

        # Load the horizontal sprite sheets
        self.blue_car_sprite_sheet = pygame.image.load("ss_blue_car.png").convert_alpha()
        self.green_car_sprite_sheet = pygame.image.load("ss_green_car.png").convert_alpha()
        self.green_truck_sprite_sheet = pygame.image.load("ss_green_truck.png").convert_alpha()
        self.barrel_sprite_sheet = pygame.image.load("ss_barrel.png").convert_alpha()
        self.chest_sprite_sheet = pygame.image.load("ss_chest.png").convert_alpha()
        self.stairs_sprite_sheet = pygame.image.load("ss_stairs.png").convert_alpha()
        self.box_sprite_sheet = pygame.image.load("ss_box.png").convert_alpha()

        self.sprites = [
            self.box_sprite_sheet,
            self.blue_car_sprite_sheet,
            self.green_car_sprite_sheet,
            self.green_truck_sprite_sheet,
            self.barrel_sprite_sheet,
            self.chest_sprite_sheet,
            self.stairs_sprite_sheet,
        ]

        self.sprite_index = 0  # Start with the first sprite sheet
        self.current_sprite = self.sprites[self.sprite_index]  # Use only the selected sprite sheet
        # Modifiable parameters
        self.mod_perspective = 45
        self.mod_scale = 2.0
        self.mod_spacing = 0.2
        self.mod_angle = 0
        self.screen_divisor = 15  # Divisor for screen size to get the top left and bottom right coordinates

        # Define locations
        self.topleft = (self.screen_size[0] / self.screen_divisor , self.screen_size[1] / self.screen_divisor)
        self.bottomright = (self.screen_size[0] - self.screen_size[0] / self.screen_divisor, self.screen_size[1] - self.screen_size[1] / self.screen_divisor)
        self.center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        self.bottomleft = (self.screen_size[0] / self.screen_divisor, self.screen_size[1] - self.screen_size[1] / self.screen_divisor)
        self.topright = (self.screen_size[0] - (self.screen_size[0] / self.screen_divisor), self.screen_size[1] / self.screen_divisor)
        
        self.locations = [self.topleft, self.topright, self.bottomleft, self.bottomright, self.center]
    
    def centre(parent : tuple, child : tuple):
            return np.divide(np.subtract(parent, child), 2)
    
    def get_slices(self, sheet):
        slice_length = min(sheet.get_width(), sheet.get_height())
        slices = []
        for i in range(sheet.get_width() // slice_length):
            rect = pygame.Rect(i * slice_length, 0, slice_length, slice_length)
            image = sheet.subsurface(rect).copy()
            slices.append(image)
        return slices
    
    
    def get_perspective_offset(self, draw_pos, focus_point, layer_index, max_total_offset=0.05, total_layers=16):
        """
        Returns an (x, y) offset for a given draw position based on its layer and distance from the focus point.
        """
        dp_vec2 = pygame.Vector2(draw_pos)  # Convert to Vector2 for easier manipulation
        fp_vec2 = pygame.Vector2(focus_point)  # Convert to Vector2 for easier manipulation

        # Calculate the normalized direction vector
        direction = (dp_vec2 - fp_vec2)
        if direction.length() == 0:
            return (0, 0)
        normalized_direction = direction.normalize()

        # Calculate the offset magnitude
        offset_magnitude = max_total_offset / total_layers

        # Apply the offset based on the layer index
        return (
            normalized_direction.x * offset_magnitude * layer_index,
            normalized_direction.y * offset_magnitude * layer_index
        )


    def draw_stack_with_optional_rotation(self, x, y, sprite_sheet, angle, scale=1, height_spacing=1.0):
        """
        Draw the rotated stack or a specific slice for debugging.
        """
        slices = self.get_slices(sprite_sheet)
        height_offset = height_spacing * scale 
        

        for i, layer in enumerate(slices):
            # Scale the layer
            original_width, original_height = layer.get_size()
            layer_scale = scale
            scaled_layer_width = int(original_width * layer_scale)
            scaled_layer_height = int(original_height * layer_scale)
            scaled_layer = pygame.transform.scale(layer, (scaled_layer_width, scaled_layer_height))

            # Create a larger surface to prevent shaking
            max_dim = int(math.sqrt((scaled_layer_width ** 2) + (scaled_layer_height ** 2)))
            larger_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)

            # Rotate the layer
            modified_layer = pygame.transform.rotate(scaled_layer, angle)
            center_of_larger_surface = (
                (larger_surface.get_width() - modified_layer.get_width()) // 2,
                (larger_surface.get_height() - modified_layer.get_height()) // 2,
            )
            larger_surface.blit(modified_layer, center_of_larger_surface)
            
            base_dimensions = larger_surface.get_size()
            base_center_x = base_dimensions[0] // 2
            base_center_y = base_dimensions[1] // 2

            x_for_perspective = x +  base_center_x
            y_for_perspective = y +  base_center_y
            # Get perspective offset
            offset_x, offset_y = self.get_perspective_offset((x_for_perspective, y_for_perspective), self.center, i, max_total_offset=10, total_layers=len(slices))

            # Final drawing position
            draw_x = x + offset_x
            draw_y = y - i * height_offset + offset_y  

            # Blit to screen
            self.screen.blit(larger_surface, (draw_x, draw_y))

    def handle_input(self):
        """Handles input with a cooldown."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return  # Skip input processing if still in cooldown

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.mod_angle += 0.1
        if keys[pygame.K_LEFT]:
            self.mod_angle -= 0.1
        self.mod_angle %= 360

        if keys[pygame.K_d]:
            sprite_slices = len(self.get_slices(self.current_sprite))
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.current_sprite = self.sprites[self.sprite_index]
        if keys[pygame.K_a]:  # Cycle through sprites
            sprite_slices = len(self.get_slices(self.current_sprite))
            self.sprite_index = (self.sprite_index - 1) % len(self.sprites)
            self.current_sprite = self.sprites[self.sprite_index]
        if keys[pygame.K_SPACE]:
            self.rotate = not self.rotate  # Reset to full stack display

        # Update the last input time
        self.last_input_time = current_time

    def update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    exit()

            # Handle input with cooldown
            self.handle_input()
            self.mod_angle += 1 # Increment angle for rotation

            self.screen.fill((30, 30, 30))
            
            # Draw the sprite stacks
            for location in self.locations:
                x, y = location
                # Draw the stack with optional rotation
                self.draw_stack_with_optional_rotation(x, y, self.current_sprite, self.mod_angle, self.mod_scale, self.mod_spacing)

            pygame.display.flip()
            self.clock.tick(60)

# Run the program
if __name__ == "__main__":
    app = SpriteStackTest()
    app.update()