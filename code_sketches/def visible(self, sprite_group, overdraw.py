def visible(self, sprite_group, overdraw_px=0):
    # 1) refresh camera BEFORE culling
    self.get_current_offset()

    sr   = self.screen_rect
    wrts = self.world_rect_to_screen  # must copy(), not mutate
    vis  = []  # collect first

    # snapshot in case group mutates elsewhere
    for sprite in list(sprite_group):
        hb = getattr(sprite, "hitbox", None) or getattr(sprite, "rect", None)
        if not hb:
            continue

        r = wrts(hb)                       # screen-space copy of full hitbox
        if overdraw_px:
            r = r.inflate(overdraw_px*2, overdraw_px*2)

        if sr.colliderect(r):
            vis.append(sprite)

    if vis:
        self.sort_sprites_by_distance_from_center(vis)
