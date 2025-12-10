#!/usr/bin/env python3
"""
Rotate each square slice in a sprite sheet by 90° and reassemble.

- Detects horizontal vs vertical sheets automatically.
- Assumes slices are square (common for MagicaVoxel exports).
- Keeps the same sheet dimensions/orientation, only rotates tiles.
- Preserves alpha.

Usage:
  python rotate_slices.py input.png
  python rotate_slices.py input_dir --out-dir rotated --suffix _rot90
  python rotate_slices.py input.png --angle 90           # 90 (CW), 270 = CCW
  python rotate_slices.py input.png --tile 16            # force tile size
  python rotate_slices.py input.png --vertical           # force vertical sheet

Requires: Pillow (pip install Pillow)
"""
import argparse
import pathlib
from typing import Tuple, List
from PIL import Image

def detect_layout(img: Image.Image, tile: int | None, force_vertical: bool | None) -> Tuple[str, int, int]:
    w, h = img.size
    if force_vertical is True:
        layout = "vertical"
        if tile is None: tile = w
        if h % tile != 0 or w != tile:
            raise ValueError(f"Vertical sheet expected width==tile and h%tile==0; got {w}x{h}, tile={tile}")
        count = h // tile
    elif force_vertical is False:
        layout = "horizontal"
        if tile is None: tile = h
        if w % tile != 0 or h != tile:
            raise ValueError(f"Horizontal sheet expected height==tile and w%tile==0; got {w}x{h}, tile={tile}")
        count = w // tile
    else:
        # auto
        if w % h == 0:
            layout, tile, count = "horizontal", h, w // h
        elif h % w == 0:
            layout, tile, count = "vertical", w, h // w
        else:
            if tile is None:
                raise ValueError("Cannot auto-detect layout. Provide --tile or force --vertical/--horizontal.")
            # try both
            if w % tile == 0 and h == tile:
                layout, count = "horizontal", w // tile
            elif h % tile == 0 and w == tile:
                layout, count = "vertical", h // tile
            else:
                raise ValueError(f"Provided tile={tile} does not fit {w}x{h}.")
    return layout, tile, count

def rotate_tile(s: Image.Image, angle: int) -> Image.Image:
    angle = angle % 360
    if angle == 90:
        return s.transpose(Image.ROTATE_270)  # PIL's ROTATE_270 = CW 90 visual
    if angle == 180:
        return s.transpose(Image.ROTATE_180)
    if angle == 270:
        return s.transpose(Image.ROTATE_90)   # PIL's ROTATE_90 = CCW 90 visual
    # arbitrary angle (rare for 90° tiles) — keep size identical
    return s.rotate(angle, expand=False, resample=Image.NEAREST)

def process_sheet(in_path: pathlib.Path, out_dir: pathlib.Path | None, suffix: str, angle: int,
                  tile: int | None, force_vertical: bool | None) -> pathlib.Path:
    img = Image.open(in_path).convert("RGBA")
    w, h = img.size
    layout, tile, count = detect_layout(img, tile, force_vertical)

    # Prepare output canvas (same size)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))

    for i in range(count):
        if layout == "horizontal":
            box = (i * tile, 0, i * tile + tile, tile)
            dst = (i * tile, 0)
        else:
            box = (0, i * tile, tile, i * tile + tile)
            dst = (0, i * tile)

        slice_img = img.crop(box)
        rotated = rotate_tile(slice_img, angle)
        out.paste(rotated, dst)

    # Build output path
    if out_dir is None:
        out_dir = in_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_name = in_path.stem + suffix + in_path.suffix
    out_path = out_dir / out_name
    out.save(out_path)
    return out_path

def iter_inputs(path: pathlib.Path) -> List[pathlib.Path]:
    if path.is_file():
        return [path]
    # directory: grab common raster extensions
    exts = {".png", ".webp", ".bmp", ".tga"}
    return [p for p in sorted(path.rglob("*")) if p.suffix.lower() in exts]

def main():
    ap = argparse.ArgumentParser(description="Rotate each tile in a sprite sheet by 90° and reassemble.")
    ap.add_argument("input", type=pathlib.Path, help="Input file or directory.")
    ap.add_argument("--out-dir", type=pathlib.Path, default=None, help="Directory for outputs.")
    ap.add_argument("--suffix", default="_rot90", help="Suffix to append to filename. Default: _rot90")
    ap.add_argument("--angle", type=int, default=90, help="Rotation angle in degrees (90, 180, 270). Default: 90 (CW)")
    ap.add_argument("--tile", type=int, default=None, help="Square tile size (px). If omitted, auto-detect.")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--vertical", action="store_true", help="Force vertical sheet (tile stacked top-to-bottom).")
    g.add_argument("--horizontal", action="store_true", help="Force horizontal sheet (tile laid left-to-right).")
    args = ap.parse_args()

    force_vertical = True if args.vertical else False if args.horizontal else None

    inputs = iter_inputs(args.input)
    if not inputs:
        raise SystemExit("No input images found.")

    for p in inputs:
        out = process_sheet(p, args.out_dir, args.suffix, args.angle, args.tile, force_vertical)
        print(f"[OK] {p.name} -> {out}")

if __name__ == "__main__":
    main()
