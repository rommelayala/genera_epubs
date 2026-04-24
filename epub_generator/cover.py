from __future__ import annotations

import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from epub_generator.config import BookConfig

_PROJECT_ROOT = Path(__file__).parent.parent
_FONTS_DIR = _PROJECT_ROOT / "fonts"


def _load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "Inter-Bold.ttf" if bold else "Inter-Regular.ttf"
    font_path = _FONTS_DIR / name
    try:
        return ImageFont.truetype(str(font_path), size)
    except (IOError, OSError):
        return ImageFont.load_default()


def generate_cover(basename: str, config: BookConfig, output_dir: Path) -> Path:
    dest = output_dir / f"{basename}.jpg"
    if dest.exists():
        return dest

    c = config.cover
    cover_title = c.title or config.title

    width, height = 600, 800
    img = Image.new("RGB", (width, height), color=c.bg_color)
    draw = ImageDraw.Draw(img)

    title_font = _load_font(c.title_size, bold=True)
    subtitle_font = _load_font(c.subtitle_size)
    footer_font = _load_font(16)

    # --- title (text wrap) ---
    max_chars = max(1, int(width * 0.85 / (c.title_size * 0.55)))
    lines = textwrap.wrap(cover_title, width=max_chars) or [cover_title]

    line_height = c.title_size + 8
    block_h = line_height * len(lines)
    y = height // 3 - block_h // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=title_font)
        lw = bbox[2] - bbox[0]
        draw.text(((width - lw) / 2, y), line, font=title_font, fill=c.text_color)
        y += line_height

    # --- subtitle ---
    if c.subtitle:
        y += 12
        bbox = draw.textbbox((0, 0), c.subtitle, font=subtitle_font)
        sw = bbox[2] - bbox[0]
        draw.text(((width - sw) / 2, y), c.subtitle, font=subtitle_font, fill=c.text_color)

    # --- accent line ---
    line_y = height - 100
    draw.line([(100, line_y), (width - 100, line_y)], fill=c.accent_color, width=1)

    # --- footer ---
    bbox = draw.textbbox((0, 0), c.footer, font=footer_font)
    fw = bbox[2] - bbox[0]
    draw.text(((width - fw) / 2, line_y + 25), c.footer, font=footer_font, fill=c.accent_color)

    output_dir.mkdir(parents=True, exist_ok=True)
    img.save(str(dest), quality=95)
    return dest
