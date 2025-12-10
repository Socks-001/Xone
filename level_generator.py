from __future__ import annotations
import csv
import random
from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import os
    

Grid = List[List[str]]  # cell values are strings for CSV friendliness

# --- simple value palette (you can remap to your project-wide IDs anytime) ---
FLOOR_VOID   = "-1"
FLOOR_SOLID  = "0"   # generic walkable
FLOOR_ROOM   = "1"   # inside a room
FLOOR_PATH   = "2"   # corridor
FLOOR_BOSS   = "3"   # boss arena

WALL_NONE    = "-1"
VALID_BLOB_MASKS = set([
    0, 1, 4, 5, 7, 16, 17, 20, 21, 23, 28, 29, 31,
    64, 65, 68, 69, 71, 80, 81, 84, 85, 87, 92, 93, 95,
    112, 113, 116, 117, 119, 124, 125, 127,
    193, 197, 199, 209, 213, 215, 221, 223,
    241, 245, 247, 253, 255
])

# For walls we’ll store the 0–255 blob mask as a string; your renderer picks the tile by mask.
ENT_EMPTY    = "-1"
ENT_PLAYER   = "100"
ENT_ENEMY    = "29"
ENT_ITEM     = "200"
ENT_HAZARD   = "300"
LIGHT_POINT  = "400"

#Decor
DECOR_EMPTY = '-1'
GRASS = "0"
GRASS_ALT = '1'
BARREL = '2'
CHEST = '3'
CRATE = '4'
LANTERN = '5'
WOOD_POST = '6'

# --- 8-way neighbor mask for blob walls (powers of two + sums) ---
NEIGH = [(-1, -1, 128), (0, -1, 1), (1, -1, 2),
         (-1,  0, 64),               (1,  0, 4),
         (-1,  1, 32),  (0,  1, 16), (1,  1, 8)]

# (dx, dy, my_bit, required_neighbor_bit)
DIRECTION_MASKS = [
    (-1, -1, 128, 8),   # upper-left: I need neighbor to connect lower-right
    ( 0, -1,   1, 16),  # up:         neighbor must connect down
    ( 1, -1,   2, 32),  # upper-right: neighbor must connect lower-left
    (-1,  0,  64, 4),   # left:       neighbor must connect right
    ( 1,  0,   4, 64),  # right:      neighbor must connect left
    (-1,  1,  32, 2),   # lower-left: neighbor must connect upper-right
    ( 0,  1,  16, 1),   # down:       neighbor must connect up
    ( 1,  1,   8, 128), # lower-right: neighbor must connect upper-left
]

def fill_decor_grass(rng: random.Random, floor: Grid, decor: Grid, p: float = 0.12):
    """Scatter grass variants on SOLID tiles only; keep rooms/paths clean."""
    H = len(floor); W = len(floor[0])
    for y in range(H):
        for x in range(W):
            if floor[y][x] == FLOOR_SOLID and rng.random() < p:
                # biased pick: 0 most common, 1/2 rarer
                r = rng.random()
                decor[y][x] = GRASS if r < 0.7 else (GRASS_ALT)

def mask8(grid: Grid, x: int, y: int, is_wall, get_mask) -> int:
    """Return a valid 0–255 blob mask considering bidirectional compatibility, with safe corner rules."""
    m = 0
    h = len(grid)
    w = len(grid[0]) if h else 0

    my_val = get_mask(x, y)
    if my_val == "X":
        my_mask = 255
    elif my_val == "20":
        my_mask = 20
    elif my_val.isdigit():
        my_mask = int(my_val)
    else:
        my_mask = 255

    for dx, dy, my_bit, required_neighbor_bit in DIRECTION_MASKS:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < w and 0 <= ny < h):
            continue

        if not is_wall(nx, ny):
            continue

        neighbor_val = get_mask(nx, ny)
        if neighbor_val == "X":
            neighbor_mask = 255
        elif neighbor_val == "20":
            neighbor_mask = 20
        elif neighbor_val.isdigit():
            neighbor_mask = int(neighbor_val)
        else:
            continue

        # --- NEW: Only allow diagonal if both adjacent edges are also walls ---
        is_diagonal = dx != 0 and dy != 0
        if is_diagonal:
            if not (is_wall(x + dx, y) and is_wall(x, y + dy)):
                continue

        if (my_mask & my_bit) and (neighbor_mask & required_neighbor_bit):
            m |= my_bit

    if m in VALID_BLOB_MASKS:
        return m
    else:
        print(f"⚠️ Invalid blob mask at ({x}, {y}) → {m}")
        return None

def carve_room_openings(floor: Grid, rects: List[Rect], min_openings: int = 2) -> set[tuple[int,int]]:
    """
    For each room, open at least `min_openings` door tiles on its border.
    Prefers spots where a corridor (FLOOR_PATH) touches the room; if not enough,
    uses midpoints on distinct sides. Returns a set of all doorway (x,y) coords.
    """
    H = len(floor); W = len(floor[0])
    doors: set[tuple[int,int]] = set()

    def neighbors4(x, y):
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < W and 0 <= ny < H:
                yield nx, ny

    for rect in rects:
        border = list(get_room_border_tiles(rect))
        room_doors: set[tuple[int,int]] = set()

        # A) Prefer openings where corridors actually meet the room
        for x, y in border:
            if any(floor[ny][nx] == FLOOR_PATH for nx, ny in neighbors4(x, y)):
                floor[y][x] = FLOOR_PATH  # carve doorway on border
                room_doors.add((x, y))
                if len(room_doors) >= min_openings:
                    break

        # B) If fewer than needed, add midpoints on distinct sides
        if len(room_doors) < min_openings:
            candidates = [
                (rect.x + rect.w // 2, rect.y),                 # top mid
                (rect.x + rect.w // 2, rect.y + rect.h - 1),    # bottom mid
                (rect.x,                 rect.y + rect.h // 2),  # left mid
                (rect.x + rect.w - 1,    rect.y + rect.h // 2),  # right mid
            ]
            # favor sides that don’t already have a door
            for x, y in candidates:
                if (x, y) not in room_doors:
                    floor[y][x] = FLOOR_PATH
                    room_doors.add((x, y))
                    if len(room_doors) >= min_openings:
                        break

        doors |= room_doors

    return doors



@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    #checks if cells in grid intersect rect 
    def cells(self):
        for yy in range(self.y, self.y + self.h):
            for xx in range(self.x, self.x + self.w):
                yield (xx, yy)

    def center(self) -> Tuple[int, int]:
        return (self.x + self.w // 2, self.y + self.h // 2)

    def inflated(self, pad: int) -> "Rect":
        return Rect(self.x - pad, self.y - pad, self.w + 2 * pad, self.h + 2 * pad)

    def intersects(self, other: "Rect") -> bool:
        return not (self.x + self.w <= other.x or
                    other.x + other.w <= self.x or
                    self.y + self.h <= other.y or
                    other.y + other.h <= self.y)

def make_grid(w: int, h: int, fill: str) -> Grid:
    return [[fill for _ in range(w)] for _ in range(h)]

def in_bounds(w: int, h: int, x: int, y: int) -> bool:
    return 0 <= x < w and 0 <= y < h

# --- room placement -----------------------------------------------------------

def place_rooms(rng: random.Random,
                floor: Grid,
                count: int = 8,
                min_sep: int = 4,
                size_range: Tuple[Tuple[int,int], Tuple[int,int]] = ((9,15),(7,11)),
                forbidden: Optional[List[Rect]] = None) -> List[Dict[str, Any]]:
    """
    Scatter axis-aligned rooms. Return metadata for each room.
    """
    H = len(floor); W = len(floor[0])
    rooms: List[Dict[str, Any]] = []
    attempts = 0
    target = count
    forbidden = forbidden or []

    while len(rooms) < target and attempts < 400:
        attempts += 1
        rw = rng.randint(*size_range[0])
        rh = rng.randint(*size_range[1])
        x = rng.randint(2, W - rw - 3)
        y = rng.randint(2, H - rh - 10)

        cand = Rect(x, y, rw, rh)
        padrect = cand.inflated(min_sep)

        if any(padrect.intersects(r['rect']) for r in rooms): continue
        if any(padrect.intersects(r) for r in forbidden): continue

        for cx, cy in cand.cells():
            floor[cy][cx] = FLOOR_ROOM

        room_data = {
            'id': len(rooms),
            'rect': cand
        }
        rooms.append(room_data)

    return rooms
# --- determine room border tiles ----------------------------------------------

def get_room_border_tiles(rect: Rect) -> set[tuple[int, int]]:
    """Return a set of (x, y) tile coordinates for the border of the given room."""
    tiles = set()

    # Top and bottom edges
    for x in range(rect.x, rect.x + rect.w):
        tiles.add((x, rect.y))                  # Top edge
        tiles.add((x, rect.y + rect.h - 1))     # Bottom edge

    # Left and right edges (excluding corners to avoid duplicates)
    for y in range(rect.y + 1, rect.y + rect.h - 1):
        tiles.add((rect.x, y))                  # Left edge
        tiles.add((rect.x + rect.w - 1, y))     # Right edge

    return tiles

# --- corridors ----------------------------------------------------------------

def carve_corridor_L(floor: Grid, a: Tuple[int,int], b: Tuple[int,int]):
    """Simple L-shaped corridor a->(bx,ay)->b; jiggle the elbow randomly."""
    ax, ay = a; bx, by = b
    elbow_first_x = random.choice([True, False])
    if elbow_first_x:
        for x in range(min(ax, bx), max(ax, bx) + 1):
            floor[ay][x] = FLOOR_PATH
        for y in range(min(ay, by), max(ay, by) + 1):
            floor[y][bx] = FLOOR_PATH
    else:
        for y in range(min(ay, by), max(ay, by) + 1):
            floor[y][ax] = FLOOR_PATH
        for x in range(min(ax, bx), max(ax, bx) + 1):
            floor[by][x] = FLOOR_PATH

def connect_rooms(rng: random.Random, floor: Grid, rooms: List[Rect]):
    """MST-ish: connect each room to nearest neighbor by center using L-corridors."""
    if not rooms: 
        return
    centers = [r["rect"].center() for r in rooms]
    unvisited = set(range(1, len(centers)))
    tree = {0}
    while unvisited:
        # find closest pair (i in tree, j in unvisited)
        best = None
        for i in list(tree):
            for j in list(unvisited):
                ax, ay = centers[i]; bx, by = centers[j]
                d = abs(ax - bx) + abs(ay - by)
                if best is None or d < best[0]:
                    best = (d, i, j)
        _, i, j = best
        carve_corridor_L(floor, centers[i], centers[j])
        tree.add(j)
        unvisited.remove(j)

# --- fill remaining floors ----------------------------------------------------

def fill_floor_noise(rng: random.Random, floor: Grid):
    """Replace VOID with SOLID (no visual variance)."""
    H = len(floor); W = len(floor[0])
    for y in range(H):
        for x in range(W):
            if floor[y][x] == FLOOR_VOID:
                floor[y][x] = FLOOR_SOLID   # always the canonical floor


# --- derive walls from floor transitions (blob mask) --------------------------

def derive_walls_from_floor(floor: Grid, wall: Grid):
    """
    For every non-walkable cell, leave -1.
    For every walkable cell that borders a non-walkable (edge of filled area),
    we compute a mask so your renderer can pick a blob tile by mask.
    """
    H = len(floor); W = len(floor[0])

    def is_walk(nx: int, ny: int) -> bool:
        if not in_bounds(W, H, nx, ny):
            return False
        return floor[ny][nx] in (FLOOR_SOLID, FLOOR_ROOM, FLOOR_PATH, FLOOR_BOSS)

    for y in range(H):
        for x in range(W):
            if wall[y][x] != WALL_NONE:
                continue  # skip tiles already set (like anchor tiles)

            if is_walk(x, y):
                
                # Build a mask of neighbors that are ALSO walkable; then the wall piece
                # around this cell is complement of that mask relative to your art choice.
                # In practice, many blob sets place "wall" where neighbor is NOT walkable,
                # so we compute mask of NOT-walk neighbors:
                def not_walk(nx, ny): return not is_walk(nx, ny)
                m = mask8(floor, x, y, not_walk)
                wall[y][x] = str(m) if m != 0 else WALL_NONE
            else:
                wall[y][x] = WALL_NONE

def derive_walls_from_border_tiles(floor: Grid, wall: Grid, border_tiles: set[tuple[int, int]]):
    H = len(floor)
    W = len(floor[0])

    # --- Step 1: Pre-fill border tiles with a temporary marker ("X") ---
    for x, y in border_tiles:
        if wall[y][x] == WALL_NONE:
            wall[y][x] = "X"  # Placeholder — not for rendering

    # --- Step 2: Define custom wall check including anchors and valid masks ---
    def is_wall(nx: int, ny: int) -> bool:
        if not in_bounds(W, H, nx, ny):
            return False
        val = wall[ny][nx]
        return (
            val == "X" or
            val == "20" or
            (val.isdigit() and int(val) in VALID_BLOB_MASKS)
        )

    # --- Step 3: Collect all "X" tiles first (so neighbors are stable) ---
    to_update = [(x, y) for x, y in border_tiles if wall[y][x] == "X"]

    # --- Step 4: Now update them all at once ---
    for x, y in to_update:
        m = mask8(wall, x, y, is_wall, lambda nx, ny: wall[ny][nx])
        wall[y][x] = str(m) if m in VALID_BLOB_MASKS else WALL_NONE



# --- dressing, hazards, items, enemies ---------------------------------------

def sprinkle_dressing(rng: random.Random, floor: Grid):
    """Disabled: keep floors canonical."""
    return


def place_hazards(rng: random.Random, floor: Grid, ent: Grid, rate: float = 0.002):
    H = len(floor); W = len(floor[0])
    for y in range(H):
        for x in range(W):
            if floor[y][x] in (FLOOR_SOLID, FLOOR_ROOM, FLOOR_PATH) and ent[y][x] == ENT_EMPTY:
                if rng.random() < rate:
                    ent[y][x] = ENT_HAZARD

def place_items(rng: random.Random, floor: Grid, ent: Grid, rate: float = 0.0015):
    H = len(floor); W = len(floor[0])
    for y in range(H):
        for x in range(W):
            if floor[y][x] in (FLOOR_ROOM,) and ent[y][x] == ENT_EMPTY:
                if rng.random() < rate:
                    ent[y][x] = ENT_ITEM

def place_enemies(rng: random.Random, floor: Grid, ent: Grid, player_cell: Tuple[int,int], rate: float = 0.002):
    H = len(floor); W = len(floor[0])
    px, py = player_cell
    for y in range(H):
        for x in range(W):
            if floor[y][x] in (FLOOR_SOLID, FLOOR_ROOM, FLOOR_PATH) and ent[y][x] == ENT_EMPTY:
                if abs(x - px) + abs(y - py) > 20 and rng.random() < rate:
                    ent[y][x] = ENT_ENEMY

# --- boss arena ---------------------------------------------------------------

def make_boss_room(floor: Grid, rng: random.Random, top_margin: int = 6, size: Tuple[int,int]=(25,18)) -> Rect:
    H = len(floor); W = len(floor[0])
    bw, bh = size
    x = max(2, W // 2 - bw // 2)
    y = top_margin
    boss = Rect(x, y, bw, bh)
    for cx, cy in boss.cells():
        floor[cy][cx] = FLOOR_BOSS
    # Add a small corridor downward to connect later
    for yy in range(boss.y + boss.h, boss.y + boss.h + 6):
        if 0 <= yy < H:
            floor[yy][x + bw // 2] = FLOOR_PATH
    return boss

# --- CSV I/O ------------------------------------------------------------------

def write_csv(path: str, grid: Grid):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerows(grid)

# --- main build API -----------------------------------------------------------

def build_level(seed: int,
                grid_w: int = 256,
                grid_h: int = 340) -> Dict[str, object]:
    rng = random.Random(seed)

    floor: Grid = make_grid(grid_w, grid_h, FLOOR_VOID)
    wall:  Grid = make_grid(grid_w, grid_h, WALL_NONE)
    ent:   Grid = make_grid(grid_w, grid_h, ENT_EMPTY)
    light: Grid = make_grid(grid_w, grid_h, ENT_EMPTY)  # keep as strings for CSV
    decor: Grid = make_grid(grid_w, grid_h, DECOR_EMPTY)

    # Player start: centered near bottom (your “center-bottom” spec)
    player_cell = (grid_w // 2, grid_h - 3)

    # Boss arena near top
    boss_rect = make_boss_room(floor, rng)
    boss_cell = boss_rect.center()

    # Place rooms with spacing; keep away from boss with a forbidden rect
    forbidden = [boss_rect.inflated(6)]
    rooms = place_rooms(rng, floor, count=8, min_sep=6, forbidden=forbidden)
    anchor_tiles = []

    # Connect rooms + boss to nearest network
    if rooms:
        # Connect rooms together
        connect_rooms(rng, floor, rooms)
        # Connect boss to nearest room center
        # pick the nearest room to the boss
        brc = boss_rect.center()
        nearest = min(rooms, key=lambda r: abs(r["rect"].center()[0] - brc[0]) + abs(r["rect"].center()[1] - brc[1]))
        carve_corridor_L(floor, brc, nearest["rect"].center())

    # Fill remaining walkables
    fill_floor_noise(rng, floor)

    # --- NEW: carve doorways before wall derivation ---
    room_rects = [r["rect"] for r in rooms]
    door_coords = carve_room_openings(floor, room_rects, min_openings=2)

    # Get room border tiles
    border_tiles = set()
    for room in rooms:
        room_border = get_room_border_tiles(room["rect"])
        # remove any cells that became doors
        room_border -= door_coords
        border_tiles.update(room_border)

        # Step C: Place anchor tile (tile 20.png) at top-left border of each room
        if room_border:
            anchor_x, anchor_y = sorted(room_border, key=lambda t: (t[0], t[1]))[0]
            wall[anchor_y][anchor_x] = "20"
            anchor_tiles.append((anchor_x, anchor_y))


    # Derive wall blob masks from anchor
    derive_walls_from_border_tiles(floor, wall, border_tiles)
    '''for x in range(0, ):  # a noticeable band within your 128x128 test grid
        wall[50][x] = "254"'''

    # Entities: player, items/hazards/enemies
    ent[player_cell[1]][player_cell[0]] = ENT_PLAYER
    sprinkle_dressing(rng, floor)
    place_hazards(rng, floor, ent)
    place_items(rng, floor, ent)
    place_enemies(rng, floor, ent, player_cell)

     # NEW: Grass after floor is finalized
    fill_decor_grass(rng, floor, decor, p=0.12)

    return {
        "floor": floor,
        "wall": wall,
        "entities": ent,
        "lights": light,
        "player_cell": player_cell,
        "boss_cell": boss_cell,
        "rooms": rooms,
        "boss_rect": boss_rect,
        "decor": decor
    }

def write_level_csvs(level: Dict[str, object], out_dir: str):
    write_csv(f"{out_dir}/floor.csv", level["floor"])
    write_csv(f"{out_dir}/wall.csv", level["wall"])
    write_csv(f"{out_dir}/entities.csv", level["entities"])
    write_csv(f"{out_dir}/lights.csv", level["lights"])
    write_csv(f"{out_dir}/decor.csv", level["decor"])


#from level_generator import build_level, write_level_csvs

def create_csv(out_dir: str = "level_data/generated",
               seed: int | None = None,
               grid_w: int = 128,
               grid_h: int = 128) -> int:
    """Build a level and write CSVs. Returns the seed used (for reproducibility)."""
    if seed is None:
        seed = random.randrange(2**31)  # why: real int seed → deterministic layouts
    lvl = build_level(seed, grid_w=grid_w, grid_h=grid_h)
    os.makedirs(out_dir, exist_ok=True)  # why: ensure folder exists
    write_level_csvs(lvl, out_dir=out_dir)
    return seed