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


class SpriteStackTest():
    def __init__(self):
        self.font = pygame.font.SysFont("atkinsonhyperlegiblemonoextralight", 18)
        self.font_small = pygame.font.SysFont("atkinsonhyperlegiblemonoextralight", 8)
        self.screen = pygame.display.get_surface()
        self.screen_size = self.screen.get_size()
        self.clock = pygame.time.Clock() 
        self.input_cooldown = 50
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
        self.mod_stack_object_height = 1
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

        
        
        self.total_layers = None  # Total number of layers in the stack

        # cache sprite stack surfaces and rects 
        self.larger_surface_cache = {}  # Cache for larger surfaces
        self.rect_cache = {}  # Cache for rects

    def centre(parent : tuple, child : tuple):
            return np.divide(np.subtract(parent, child), 2)
    
    def get_slices(self, sheet):
        slice_length = min(sheet.get_width(), sheet.get_height())
        slices = []
        for i in range(sheet.get_width() // slice_length):
            rect = pygame.Rect(i * slice_length, 0, slice_length, slice_length)
            image = sheet.subsurface(rect).copy()
            slices.append(image)
            self.total_layers = len(slices)  # Update total layers based on the number of slices
            #print (f'total layers = {self.total_layers}')
        return slices  
    
    def get_perspective_offset(self, surface_pos, focus_point, layer_index, stack_object_height, total_layers=None):
        """
        Calculates the perspective offset for a given layer in the sprite stack.

        This method determines how much each layer in the stack should be offset
        based on its position relative to a focus point, creating a pseudo-3D perspective effect.

        :param surface_pos: A tuple (x, y) representing the base position of the layer being drawn.
        :param focus_point: A tuple (x, y) representing the focus point (e.g., the camera or perspective center).
        :param layer_index: The index of the current layer in the stack (0-based).
        :param max_total_offset: The maximum offset (in pixels) to apply across all layers. Defaults to 10.
        :param total_layers: The total number of layers in the stack. Defaults to 16.
        :return: A tuple (offset_x, offset_y) representing the calculated perspective offset for the layer.
        """
        if total_layers is None:
            total_layers = self.total_layers
        
        #print (f'total layers = {total_layers}')

        direction = pygame.Vector2(surface_pos) - pygame.Vector2(focus_point)
        
        # Normalize the direction vector to get the unit vector
        if direction.length() == 0:    
            return (0, 0)
        

        #print (f'draw position = {draw_pos} focus point = {focus_point} normalized direction = {normalized_direction}')

        # Calculate the offset magnitude
        offset_magnitude = (stack_object_height / total_layers) * direction.length() / (self.screen_size[0] / 2)

        direction.normalize_ip()
        #print(f"Layer {layer_index}: direction = {direction}, offset = ({direction.x * offset_magnitude * layer_index}, {direction.y * offset_magnitude * layer_index})")

        # Apply the offset based on the layer index
        return (
            direction.x * offset_magnitude * layer_index,
            direction.y * offset_magnitude * layer_index
        )

    def draw_text(self, text, pos, small=False):
        """
        Renders and draws text on the screen at the specified position.

        :param text: The string to render and display.
        :param pos: A tuple (x, y) representing the position where the text will be drawn. 
                    The text will be centered at this position.
        :param small: A boolean indicating whether to use the smaller font. 
                    If True, the smaller font (`self.font_small`) is used; otherwise, the default font (`self.font`) is used.
        """

        if small:
            text_surface = self.font_small.render(text, False, (255, 255, 255))
            text_rect = text_surface.get_rect(center=pos)
            self.screen.blit(text_surface, text_rect)
        else:
            text_surface = self.font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=pos)
            self.screen.blit(text_surface, text_rect)

    def draw_dashed_rect(self, surface, color, rect, dash_length=5, space_length=3, width=1, alpha=128):
        """
        Draws a dashed rectangle on the given surface with alpha transparency.

        :param surface: The Pygame surface to draw on.
        :param color: The color of the dashes (e.g., (255, 0, 0) for red).
        :param rect: A pygame.Rect object defining the rectangle.
        :param dash_length: The length of each dash.
        :param space_length: The length of the space between dashes.
        :param width: The thickness of the dashes.
        :param alpha: The transparency of the dashes (0 = fully transparent, 255 = fully opaque).
        """
        x, y, w, h = rect

        # Create a transparent surface for the dashed rectangle
        dashed_surface = pygame.Surface((w, h), pygame.SRCALPHA)
        dashed_surface.set_alpha(alpha)

        # Top edge
        for i in range(x, x + w, dash_length + space_length):
            pygame.draw.line(dashed_surface, color, (i - x, 0), (min(i + dash_length, x + w) - x, 0), width)

        # Bottom edge
        for i in range(x, x + w, dash_length + space_length):
            pygame.draw.line(dashed_surface, color, (i - x, h - 1), (min(i + dash_length, x + w) - x, h - 1), width)

        # Left edge
        for i in range(y, y + h, dash_length + space_length):
            pygame.draw.line(dashed_surface, color, (0, i - y), (0, min(i + dash_length, y + h) - y), width)

        # Right edge
        for i in range(y, y + h, dash_length + space_length):
            pygame.draw.line(dashed_surface, color, (w - 1, i - y), (w - 1, min(i + dash_length, y + h) - y), width)

        # Blit the dashed surface onto the main surface
        surface.blit(dashed_surface, (x, y))
    
    def get_surface_center(self, surface):
        """
        Returns the center (x, y) coordinates of a Pygame surface. Especially useful for positioning elements without rects.

        :param surface: The Pygame surface to calculate the center for.
        :return: A tuple (center_x, center_y) representing the center of the surface.
        """
        center_x = surface.get_width() // 2
        center_y = surface.get_height() // 2
        return center_x, center_y
    
    def draw_point(self, surface, pos=None, color=(255, 0, 0, 255)):
        """
        Draws a single point (1px) on the given screen at the specified position, considering alpha transparency.

        :param surface: The Pygame surface to draw on.
        :param pos: A tuple (x, y) representing the position of the point on the screen. Defaults to the center of the surface.
        :param color: A tuple (R, G, B, A) representing the color and alpha transparency of the point.
        """
        # If pos is None, calculate the center of the surface
        if pos is None:
            pos = self.get_surface_center(surface)

        # Create a 1x1 surface with an alpha channel
        point_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        
        # Fill the surface with the color (including alpha)
        point_surface.fill(color)
        
        # Blit the point surface onto the screen at the specified position
        surface.blit(point_surface, pos)

    def draw_sprite_stack(self, x, y, sprite_sheet, angle, scale=1.0, height_spacing=1.0, perspective = 10):
        """
        Draws a stack of rotated and scaled sprite layers at a specified position, with optional perspective and spacing.

        :param x: The x-coordinate of the base position for the stack.
        :param y: The y-coordinate of the base position for the stack.
        :param sprite_sheet: The sprite sheet containing horizontal slices to stack.
        :param angle: The rotation angle (in degrees) to apply to each layer.
        :param scale: The scaling factor for the layers. Defaults to 1 (no scaling).
        :param height_spacing: The vertical spacing between layers in the stack. Defaults to 1.0.
        :param perspective: The perspective angle (in degrees) to apply to the stack. Defaults to 10.
        """
        slices = self.get_slices(sprite_sheet)
        perspective_scale = math.cos(math.radians(perspective))
        height_offset = height_spacing * scale * perspective_scale

        for i, layer in enumerate(slices):
            # Scale the layer
            original_width, original_height = layer.get_size()
            #layer_scale = scale
            #layer_scale = round(scale + (i * 0.01), 2) # Adjust the scaling factor for each layer
            scaled_layer_width = original_width + i
            scaled_layer_height = original_height + i
            scaled_layer = pygame.transform.scale(layer, (scaled_layer_width, scaled_layer_height))

            # Check if the larger surface for this layer is already cached
            '''cache_key = i
            if cache_key in self.larger_surface_cache:
                larger_surface = self.larger_surface_cache[cache_key]
            else:
                # Create a larger surface to prevent shaking
                max_dim = int(math.sqrt((scaled_layer_width ** 2) + (scaled_layer_height ** 2)))
                larger_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)
                self.larger_surface_cache[cache_key] = larger_surface  # Cache the larger surface'''
            
            # Create a larger surface to prevent shaking
            max_dim = int(math.sqrt((scaled_layer_width ** 2) + (scaled_layer_height ** 2)))
            larger_surface = pygame.Surface((max_dim, max_dim), pygame.SRCALPHA)
            
           
            # print (f'cache total = {len(self.larger_surface_cache)}')
            # Rotate the layer
            rotated = pygame.transform.rotate(scaled_layer, angle)
            center_of_larger_surface = (
                (larger_surface.get_width() - rotated.get_width()) // 2,
                (larger_surface.get_height() - rotated.get_height()) // 2,
            )

            larger_surface.fill((170, 100, 150, 5))
            larger_surface.blit(rotated, center_of_larger_surface)

            rect = larger_surface.get_rect(center=(x, y))


            # Cache the rect for this layer
            

            # Get the center of the larger surface           
            '''base_center_x = larger_surface.get_width() // 2
            base_center_y = larger_surface.get_height() // 2
            base_center = (base_center_x, base_center_y)'''

            
            # Get perspective offset
            offset_x, offset_y = self.get_perspective_offset((x , y), 
                                                             self.center, i, stack_object_height = self.mod_stack_object_height, total_layers=len(slices)
                                                             )
            

            #draw_pos = (x + offset_x, y - height_offset + offset_y)
            draw_pos = (x + i * offset_x, y + i * offset_y)
            #print (f'offset = {offset_y} y offset = {y + (i + offset_y)}')
            print (f'offset = {offset_x} y offset = {x + (i + offset_x)}')
            rect.center = draw_pos  # Update the rect position based on the calculated draw position
            #print (f'{i} offset = {offset_x} {offset_y}')

            # Blit to screen
            self.screen.blit(larger_surface, rect.topleft)
            #pygame.draw.rect(self.screen, (255,0,0), rect, width=1)
            self.draw_dashed_rect(self.screen, (255, 0, 0, 20), rect, dash_length=5, space_length=3, width=1, alpha=128)

    def handle_input(self):
        """
        Handles user input for controlling sprite movement, rotation, and toggling settings.

        - Movement: Arrow keys (UP, DOWN, LEFT, RIGHT) move the sprite position.
        - Rotation: 'A' and 'D' keys rotate the sprite stack counterclockwise and clockwise, respectively.
        - Toggle Placement Mode: 'C' key toggles between center-based and top-left-based placement.
        - Sprite Switching: SPACE key switches to the next sprite in the list, with a cooldown to prevent rapid switching.

        :return: None
        """
        keys = pygame.key.get_pressed()
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
            self.mod_stack_object_height -= 1
        if keys[pygame.K_d]:
            self.mod_stack_object_height += 1
        

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
            self.mod_angle %= 360 # Keep angle within 0-359 degrees

            self.screen.fill((30, 30, 30))
            
            
            for location in self.locations:
                x, y = location
                # Draw the stack with optional rotation
                self.draw_sprite_stack(x, y, self.current_sprite, self.mod_angle, self.mod_scale, self.mod_spacing)
                
            self.draw_point (self.screen, self.center, color=(157, 255, 0, 255))
            self.draw_text(f"cen = {(x,y)}", (x + 64, y), True)
            self.draw_text(f'screen size = {self.screen_size}', (self.locations[1][0] - 50, self.locations[1][1]), small=True)
            self.draw_text(f'object height = {self.mod_stack_object_height}', (self.locations[1][0] - 50, self.locations[1][1] + 10), small=True)
            pygame.display.flip()
            self.clock.tick(60)

# Run the program
if __name__ == "__main__":#
    app = SpriteStackTest()
    app.update()