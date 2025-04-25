from copyreg import remove_extension
from csv import reader
from os import walk
import pygame
from sys import exit
import pathlib



def import_csv_layout(path):
    terrain_map = []

    with open(path) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map

def str_to_int(text: str):
    """Given a string, returns the int embedded within it, e.g. 'text12text3txt4' -> 1234"""
    digits = "".join(c for c in text if (ord('0') <= ord(c) <= ord('9')))
    return int(digits) if len(digits) > 0 else 0

def import_folder (path):
    
    surface_list = []

    for _,__,img_files in walk(path): 
        img_files = sorted(img_files)
        for image in img_files:
            full_path = path + '/' + image
            #print(full_path)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
            # Debug: Print loaded image paths
            print(f"Loaded image: {full_path}")   
    
    return surface_list

def counter (element):
    amount = 0 
    for i in element:
        amount += 1

    return amount  

def get_surface_center(surface):
    """
    Returns the center (x, y) coordinates of a Pygame surface. Especially useful for positioning elements without rects.

    :param surface: The Pygame surface to calculate the center for.
    :return: A tuple (center_x, center_y) representing the center of the surface.
    """
    center_x = surface.get_width() // 2
    center_y = surface.get_height() // 2
    return center_x, center_y

def draw_point(surface, pos=None, color=(255, 0, 0, 255)):
    """
    Draws a single point (1px) on the given screen at the specified position, considering alpha transparency.

    :param surface: The Pygame surface to draw on.
    :param pos: A tuple (x, y) representing the position of the point on the screen. Defaults to the center of the surface.
    :param color: A tuple (R, G, B, A) representing the color and alpha transparency of the point.
    """
    # If pos is None, calculate the center of the surface
    if pos is None:
        pos = get_surface_center(surface)

    # Create a 1x1 surface with an alpha channel
    point_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
    
    # Fill the surface with the color (including alpha)
    point_surface.fill(color)
    
    # Blit the point surface onto the screen at the specified position
    surface.blit(point_surface, pos)

def quit():
    print("Quitting game...")
    pygame.quit()
    exit()

def search_dict(d, key):
    """Recursively search for a key in a nested dictionary."""
    if isinstance(d, dict):  # If d is a dictionary
        for k, v in d.items():
            if k == key:
                return v
            elif isinstance(v, dict):  # If the value is another dictionary, search it
                result = search_dict(v, key)
                if result is not None:
                    return result
    return None  # Return None if key isn't found

def init_audio():
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    print("Audio initialized.")
    #midi is available 