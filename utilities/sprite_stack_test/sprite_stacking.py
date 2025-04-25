import pygame
import math
import os
import sys
import numpy as np
import pygame.freetype

# Set the working directory to the directory of the script
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

pygame.init()

class screen_setup:
    screen_size = 256
    screen = pygame.display.set_mode((screen_size, screen_size), pygame.SCALED)
    pygame.display.set_caption("Sprite Stack Test")


class SpriteStackTest:
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 18, bold=True)
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock() 
        self.input_cooldown = 1000
        self.last_input_time = 0  

        # Load the horizontal sprite sheets
        self.sprites = [
            pygame.image.load("ss_box.png").convert_alpha(),
            pygame.image.load("ss_blue_car.png").convert_alpha(),
            pygame.image.load("ss_green_car.png").convert_alpha(),
            pygame.image.load("ss_green_truck.png").convert_alpha(),
            pygame.image.load("ss_barrel.png").convert_alpha(),
            pygame.image.load("ss_chest.png").convert_alpha(),
            pygame.image.load("ss_stairs.png").convert_alpha(),
        ]

        self.sprite_index = 0  # Start with the first sprite sheet
        self.current_sprite = self.sprites[self.sprite_index]  # Use only the selected sprite sheet
        
        # Modifiable parameters
        self.mod_perspective = 45
        self.mod_scale = 2.0
        self.mod_spacing = 0.05
        self.mod_angle = 0
        self.screen_divisor = 15  

        # CHANGED: Added position for sprite movement
        self.sprite_pos = [self.screen_size[0] // 2, self.screen_size[1] // 2]

        # Define locations
        w, h = self.screen_size
        self.center = (w / 2, h / 2)
        d = self.screen_divisor
        self.locations = [
            (w / d, h / d),                 # top-left
            (w - w / d, h / d),            # top-right
            (w / d, h - h / d),            # bottom-left
            (w - w / d, h - h / d),        # bottom-right
            (w / 2, h / d),                # top-center
            (w / 2, h - h / d),            # bottom-center
            (w / d, h / 2),                # left-center
            (w - w / d, h / 2),            # right-center
            self.center                   # center
        ]

        # Toggle to switch between top-left and center-based placement
        self.use_center_based = True  # True means center-based, False means top-left based

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
    
    
    def get_perspective_offset(self, draw_pos, focus_point, layer_index, max_total_offset=10, total_layers=16):
        direction = pygame.Vector2(draw_pos) - pygame.Vector2(focus_point)

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

    # Add this method to the class
    def draw_text(self, text, pos):
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=pos)
        self.screen.blit(text_surface, text_rect)

    def draw_point(self, pos):
        pygame.draw.line(self.screen, (255, 0, 0), (pos[0], pos[1]), (pos[0], pos[1]))
    def draw_stack_with_optional_rotation(self, x, y, sprite_sheet, angle, scale=1, height_spacing=1.0, perspective = 10):
        """
        Draw the rotated stack or a specific slice for debugging.
        """
        slices = self.get_slices(sprite_sheet)
        perspective_scale = math.cos(math.radians(perspective))
        height_offset = height_spacing * scale * perspective_scale
        

        for i, layer in enumerate(slices):
            # Scale the layer
            original_width, original_height = layer.get_size()
            #layer_scale = scale
            layer_scale = round(scale * 1 + (i * 0.02), 2) # Adjust the scaling factor for each layer
            scaled_layer_width = original_width * layer_scale
            scaled_layer_height = original_height * layer_scale
            scaled_layer = pygame.transform.scale(layer, (scaled_layer_width, scaled_layer_height))

            # Create a larger surface to prevent shaking
            max_dim = int(math.sqrt((scaled_layer_width ** 2) + (scaled_layer_height ** 2)))
            larger_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)

            # Rotate the layer
            rotated = pygame.transform.rotate(scaled_layer, angle)
            center_of_larger_surface = (
                (larger_surface.get_width() - rotated.get_width()) // 2,
                (larger_surface.get_height() - rotated.get_height()) // 2,
            )

            larger_surface.fill((170, 100, 150, 5))
            larger_surface.blit(rotated, center_of_larger_surface)

            # Get the center of the larger surface           
            base_center_x = larger_surface.get_width() // 2
            base_center_y = larger_surface.get_height() // 2
            base_center = (base_center_x, base_center_y)
            self.draw_point(base_center)
            

            # Get perspective offset
            offset_x, offset_y = self.get_perspective_offset((x +  base_center_x, y +  base_center_y), 
                                                             self.center, i, max_total_offset=10, total_layers=len(slices)
                                                             )
            # Final drawing position
            if self.use_center_based:
                # Center-based placement
                draw_x = (x + offset_x) - base_center_x
                draw_y = (y - i * height_offset + offset_y) - base_center_y
            else:
                draw_x = x + offset_x
                draw_y = y - i * height_offset + offset_y  

            # Blit to screen
            self.screen.blit(larger_surface, (draw_x, draw_y))

    def handle_input(self):
        keys = pygame.key.get_pressed()
                # Toggle to switch between top-left and center-based placement
        if keys[pygame.K_c]:  # Press C to toggle between center-based and top-left-based
            self.use_center_based = not self.use_center_based
        # CHANGED: Movement keys
        if keys[pygame.K_LEFT]:
            self.sprite_pos[0] -= 4
        if keys[pygame.K_RIGHT]:
            self.sprite_pos[0] += 4
        if keys[pygame.K_UP]:
            self.sprite_pos[1] -= 4
        if keys[pygame.K_DOWN]:
            self.sprite_pos[1] += 4

        # CHANGED: Rotation with A / D
        if keys[pygame.K_a]:
            self.mod_angle -= 1
        if keys[pygame.K_d]:
            self.mod_angle += 1
        self.mod_angle %= 360

        # CHANGED: Sprite switching on SPACE with cooldown
        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and (current_time - self.last_input_time > self.input_cooldown):
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites)
            self.current_sprite = self.sprites[self.sprite_index]
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
            
            
            '''for location in self.locations:
                x, y = location
                # Draw the stack with optional rotation
                self.draw_stack_with_optional_rotation(x, y, self.current_sprite, self.mod_angle, self.mod_scale, self.mod_spacing)
                self.draw_point((x,y))
            self.draw_text(f"cen = {self.use_center_based}", self.locations[3])'''

            # CHANGED: Use self.sprite_pos for positioning
            x, y = self.sprite_pos
            self.draw_stack_with_optional_rotation(x, y, self.current_sprite, self.mod_angle, self.mod_scale, self.mod_spacing)

            pygame.display.flip()
            self.clock.tick(60)

# Run the program
if __name__ == "__main__":
    app = SpriteStackTest()
    app.update()