from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from tp2_common import load_image, read_csv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a visual contact sheet from a TP2 top-k CSV.")
    parser.add_argument("--top", type=Path, required=True, help="Path to top3.csv or equivalent.")
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--thumb-size", type=int, default=192)
    return parser.parse_args()


def fit_square(image: Image.Image, size: int) -> Image.Image:
    image = image.copy()
    image.thumbnail((size, size), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (size, size), "white")
    x = (size - image.width) // 2
    y = (size - image.height) // 2
    canvas.paste(image, (x, y))
    return canvas


def draw_label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, font: ImageFont.ImageFont) -> None:
    x, y = xy
    draw.rectangle((x, y, x + 180, y + 18), fill=(255, 255, 255))
    draw.text((x + 4, y + 2), text, fill=(0, 0, 0), font=font)


def main() -> None:
    args = parse_args()
    rows = read_csv(args.top)
    if not rows:
        raise ValueError(f"No rows in {args.top}")

    by_target: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        by_target.setdefault(row["target_name"], []).append(row)
    for group in by_target.values():
        group.sort(key=lambda item: int(item["rank"]))

    thumb = args.thumb_size
    gap = 16
    label_height = 24
    columns = 4
    width = columns * thumb + (columns + 1) * gap
    row_height = thumb + label_height + gap
    height = len(by_target) * row_height + gap

    sheet = Image.new("RGB", (width, height), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for row_index, target_name in enumerate(sorted(by_target)):
        y = gap + row_index * row_height
        group = by_target[target_name]
        target = fit_square(load_image(group[0]["target_path"]), thumb)
        x = gap
        sheet.paste(target, (x, y + label_height))
        draw_label(draw, (x, y), f"{target_name} target", font)

        for col_index, row in enumerate(group[:3], start=1):
            x = gap + col_index * (thumb + gap)
            render = fit_square(load_image(row["render_path"]), thumb)
            sheet.paste(render, (x, y + label_height))
            draw_label(draw, (x, y), f"rank {row['rank']} cand {row['candidate_index']}", font)

    output = args.output or (args.top.parent / "contact_sheet_top3.jpg")
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)
    print("Wrote:", output)


if __name__ == "__main__":
    main()
