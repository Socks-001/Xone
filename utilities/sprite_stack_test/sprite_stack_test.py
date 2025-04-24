import pygame
import math
import os
import sys

# This is a test by Forgotten Druid to test the sprite stack and rotation in python 3 and pygame-ce 
# there is an issue that arises when rotationg where a jitter occurs when the sprite is rotated
# this is due to a combination of squares creating longer dimensions on diagonals and the surface cropping to this new dimension
# that way the previos frame (surface size) is not the same as the current frame (surface size), and the image isnt "centered" on the screen
# Ultimately the problem is resolved byt rotating the image and then applying it to a larger surface, which is then blitted to the screen
# I'm sure this can be imporoved upon and there are hard coded values but this is more a demonsration of the concept than a final product
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
        self.input_cooldown = 50  # Cooldown in milliseconds
        self.last_input_time = 0  # Tracks the last time an input was processed

        # Load the horizontal sprite sheets
        self.blue_car_sprite_sheet = pygame.image.load("ss_blue_car.png").convert_alpha()
        self.green_car_sprite_sheet = pygame.image.load("ss_green_car.png").convert_alpha()
        self.green_truck_sprite_sheet = pygame.image.load("ss_green_truck.png").convert_alpha()
        self.barrel_sprite_sheet = pygame.image.load("ss_barrel.png").convert_alpha()
        self.chest_sprite_sheet = pygame.image.load("ss_chest.png").convert_alpha()
        self.stairs_sprite_sheet = pygame.image.load("ss_stairs.png").convert_alpha()

        self.sprites = [
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
        self.mod_spacing = 1.0
        self.mod_angle = 0

        # Define locations
        location_topleft = (32, 32)
        location_bottomright = (self.screen_size[0] - 32, self.screen_size[1] - 32)
        location_center = (self.screen_size[0] / 2, self.screen_size[1] / 2)
        location_bottomleft = (32, self.screen_size[1] - 32)
        location_topright = (self.screen_size[0] - 32, 32)

        self.topleft_rect = pygame.Rect(location_topleft, (self.screen_size[0] /10, self.screen_size[1] / 10))
        self.locations = [location_topleft, location_bottomright, location_center, location_bottomleft, location_topright]

    def get_slices(self, sheet):
        slice_length = min(sheet.get_width(), sheet.get_height())
        slices = []
        for i in range(sheet.get_width() // slice_length):
            rect = pygame.Rect(i * slice_length, 0, slice_length, slice_length)
            image = sheet.subsurface(rect).copy()
            slices.append(image)
        return slices
    
    def get_perspective_offset(self, draw_pos, focus_point, layer_index, max_offset=20):
        """
        Returns an (x, y) offset for a given draw position based on its layer and distance from the focus point.
        The higher the layer_index, the more offset is applied.
        """
        dx = draw_pos[0] - focus_point[0]
        dy = draw_pos[1] - focus_point[1]
        distance = math.hypot(dx, dy)
        if distance == 0:
            return (0, 0)

        norm_dx = dx / distance
        norm_dy = dy / distance

        perspective_strength = min(layer_index * 0.5, max_offset)
        return (norm_dx * perspective_strength, norm_dy * perspective_strength)


    def draw_stack_with_optional_rotation(self, x, y, sprite_sheet, angle, scale=1, height_spacing=1.0, perspective=10):
        """
        Draw the rotated stack or a specific slice for debugging.
        """
        slices = self.get_slices(sprite_sheet)
        perspective_scale = math.cos(math.radians(perspective))
        height_offset = height_spacing * scale * perspective_scale
        
        scaled_slices_container = []
        scaled_and_rotated_container = []
        larger_surface_container = []

        for i, layer in enumerate(slices):

            # create scaled image layer and append to container 
            original_width, original_height = layer.get_size()
            #layer_scale = scale * (1 + i * 0.01)  # Adjust scale based on layer index
            layer_scale = scale   # Adjust scale based on layer index
            scaled_layer_width = int(original_width * layer_scale)
            scaled_layer_height = int(original_height * layer_scale)
            scaled_layer = pygame.transform.scale(layer, (scaled_layer_width, scaled_layer_height))
            scaled_slices_container.append(scaled_layer)

            # Create a larger surface to prevent shaking
            max_dim = int(math.sqrt((scaled_layer_width**2)+ (scaled_layer_height**2)))  # Diagonal of the layer
            larger_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)
            larger_surface.fill((170, 100, 150, 10))  # Translucent background
            
            
            # Rotate layer by the mod_angle
            modified_layer = pygame.transform.rotate(scaled_layer, angle)
            scaled_and_rotated_container.append(modified_layer)
            
            center_of_larger_surface = ((larger_surface.get_width() - modified_layer.get_width()) // 2, (larger_surface.get_height() - modified_layer.get_height()) // 2)
            
            larger_surface.blit(modified_layer, center_of_larger_surface)  # Blit the rotated layer to the larger surface
            larger_surface_container.append(larger_surface)  # Update the modified_slices list with the rotated layer
           

        # Blit each scaled container layers to the screen (with "perspective")
        for i, layer in enumerate(scaled_slices_container):

            # Blit the layer
            self.screen.blit(layer, (x,y - i * height_offset))

            # Draw a debug box around the layer
            #scaled_debug_rect = layer.get_rect()
            #pygame.draw.rect(self.screen, (255, 10, 10), scaled_debug_rect, 1)  # Red box with 1-pixel thickness

        # Blit each scaled and rotated container layers to the screen (with "perspective")
        for i, layer in enumerate(scaled_and_rotated_container):

            # Blit the layer
            self.screen.blit(layer, (x + 64,y - i * height_offset))

            # Draw a debug box around the layer
            scaled_debug_rect = layer.get_rect(topleft=(x + 64, y - i * height_offset))
            pygame.draw.rect(self.screen, (255, 10, 10), scaled_debug_rect, 1)  # Red box with 1-pixel thickness
        
        # Blit modified layer blitted to secondarly larger surfaces container layers to the screen (with "perspective")
        for i, layer in enumerate(larger_surface_container):

            # Blit the layer
            self.screen.blit(layer, (x + 128,y - i * height_offset))

            # Draw a debug box around the layer
            larger_debug_rect = layer.get_rect(topleft=(x + 128, y - i * height_offset))
            pygame.draw.rect(self.screen, (10, 255, 10), larger_debug_rect, 1)  # Red box with 1-pixel thickness
        


    def handle_input(self):
        """Handles input with a cooldown."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_input_time < self.input_cooldown:
            return  # Skip input processing if still in cooldown

        keys = pygame.key.get_pressed()
        
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

            self.screen.fill((30, 30, 30))
            self.mod_angle +=1
            self.mod_angle %= 360

            self.draw_stack_with_optional_rotation(32, (self.screen_size[1] / 2) - 16, self.sprites[self.sprite_index], self.mod_angle, self.mod_scale, self.mod_spacing, self.mod_perspective)

            '''for location in self.locations:
                pos_x, pos_y = location
                sprite = self.current_sprite  # Use the stairs sprite sheet for all locations
                self.draw_stack_with_optional_rotation(pos_x, pos_y, sprite, self.mod_angle, self.mod_scale, self.mod_spacing, self.mod_perspective, True)'''
            pygame.display.flip()
            self.clock.tick(60)

# Run the program
if __name__ == "__main__":
    app = SpriteStackTest()
    app.update()