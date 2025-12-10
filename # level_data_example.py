# level_data_example.py
from utilities import import_csv_layout
import pygame, os

level = {
    'level_config': {
        'game': None,
        'game_running': True,
        'level_running': True,
        'visible_sprites': None,
        'obstacle_sprites': None,
        'level_index': 0,
        'level_list': ['generated']  # <- point at new level name
    }
}

def load_blob_masks_folder(path, prefix="test_blob_", ext=".png"):
    """Return {mask_int: Surface} by parsing filenames like test_blob_95.png."""
    table = {}
    if not os.path.isdir(path): return table
    for name in sorted(os.listdir(path)):
        if not name.endswith(ext): continue
        stem = name[:-len(ext)]
        if not stem.startswith(prefix): continue
        try:
            mask = int(stem[len(prefix):])
        except ValueError:
            continue
        surf = pygame.image.load(os.path.join(path, name)).convert_alpha()
        table[mask] = surf
    return table

def load_level_folder(name: str, folder: str):
    # CSV layouts
    floor_layout = import_csv_layout(f'level_data/{folder}/floor.csv')
    wall_layout  = import_csv_layout(f'level_data/{folder}/wall.csv')
    ent_layout   = import_csv_layout(f'level_data/{folder}/entities.csv')
    light_layout = import_csv_layout(f'level_data/{folder}/lights.csv')

    # Graphics:
    #  - floors: put your floor tiles in graphics/floor/ (e.g., floor_0.png, floor_1.png ...)
    #  - walls:  your 47 blob tiles live in graphics/level_tiles/test_blob_*.png
    floor_graphics = []
    floor_dir = 'graphics/floor'
    if os.path.isdir(floor_dir):
        for fn in sorted(os.listdir(floor_dir)):
            if fn.lower().endswith('.png'):
                floor_graphics.append(pygame.image.load(os.path.join(floor_dir, fn)).convert_alpha())
    walls_by_mask = load_blob_masks_folder('graphics/level_tiles')

    level[name] = {
        'floor_layout': floor_layout,
        'wall_layout': wall_layout,
        'entity_layout': ent_layout,
        'lights_layout': light_layout,
        'floor_graphics': floor_graphics,
        'walls_by_mask': walls_by_mask,
    }

# call this once on import (or from main)
load_level_folder('generated', 'generated')
