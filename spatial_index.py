# spatial_index.py
import pygame
from collections import defaultdict

class ChunkIndex:
    def __init__(self, tilesize: int, chunk_tiles: int = 16):
        self.tilesize = tilesize
        self.chunk_tiles = chunk_tiles
        self.chunk_px = tilesize * chunk_tiles
        self.buckets = defaultdict(list)
        self._sprite_bucket = {}  # sprite -> (cx, cy)

    def _chunk_coords_from_point(self, x: float, y: float):
        return (int(x) // self.chunk_px, int(y) // self.chunk_px)

    def _chunk_coords_from_rect(self, rect: pygame.Rect | pygame.FRect):
        left = int(rect.left) // self.chunk_px
        right = int(rect.right - 1) // self.chunk_px
        top = int(rect.top) // self.chunk_px
        bottom = int(rect.bottom - 1) // self.chunk_px
        return left, right, top, bottom

    def clear(self):
        self.buckets.clear()
        self._sprite_bucket.clear()

    def add(self, sprite):
        # use hitbox if you have it
        r = getattr(sprite, "hitbox", sprite.rect)
        cx, cy = self._chunk_coords_from_point(r.centerx, r.centery)
        self.buckets[(cx, cy)].append(sprite)
        self._sprite_bucket[sprite] = (cx, cy)

    def remove(self, sprite):
        key = self._sprite_bucket.pop(sprite, None)
        if key is None:
            return
        lst = self.buckets.get(key)
        if not lst:
            return
        # remove by identity
        try:
            lst.remove(sprite)
        except ValueError:
            pass

    def update(self, sprite):
        r = getattr(sprite, "hitbox", sprite.rect)
        new_key = self._chunk_coords_from_point(r.centerx, r.centery)
        old_key = self._sprite_bucket.get(sprite)
        if old_key == new_key:
            return
        if old_key is not None:
            lst = self.buckets.get(old_key)
            if lst:
                try:
                    lst.remove(sprite)
                except ValueError:
                    pass
        self.buckets[new_key].append(sprite)
        self._sprite_bucket[sprite] = new_key

    def build_static(self, group):
        # for tiles/walls/set_dressing that never move
        for spr in group:
            self.add(spr)

    def query_rect(self, rect: pygame.Rect | pygame.FRect):
        l, r, t, b = self._chunk_coords_from_rect(rect)
        out = []
        append = out.append
        for cy in range(t, b + 1):
            for cx in range(l, r + 1):
                for spr in self.buckets.get((cx, cy), ()):
                    append(spr)
        return out

