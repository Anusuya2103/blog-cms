#!/usr/bin/env python3
"""
BlogCMS - LinkedIn showcase asset generator
==========================================
Builds the images used in the LinkedIn post / README hero:

  assets/banner.png           1200x627  link-preview / hero banner
  assets/carousel/01..05.png  1080x1350 document-post cards (4:5, the format
                              LinkedIn renders best)

Both are generated purely from the screenshots already captured in
demo/shots/, so no design tooling is required.

Usage:
    python demo/make_showcase.py
"""
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
SHOTS = BASE / "demo" / "shots"
ASSETS = BASE / "assets"
CAROUSEL = ASSETS / "carousel"

# Palette lifted from frontend/src/index.css so the assets match the app UI.
INK = "#15181e"
INK_SOFT = "#5b6470"
BG = "#f6f5f2"
SURFACE = "#ffffff"
ACCENT = "#2b5cb8"
ACCENT_DARK = "#1e4489"
BORDER = "#e5e1d8"
DARK_BG = "#0f1218"
DARK_PANEL = "#171b23"
GREEN = "#3fb950"

FONT_DIR = Path("C:/Windows/Fonts")
REGULAR = FONT_DIR / "arial.ttf"
BOLD = FONT_DIR / "arialbd.ttf"
MONO = FONT_DIR / "consola.ttf"
MONO_BOLD = FONT_DIR / "consolab.ttf"


def autocrop(img: Image.Image, pad: int = 14) -> Image.Image:
    """Trim the uniform background around a screenshot.

    The captured terminal shots have large empty margins (a dark canvas
    around a small window). Cropping to the actual content keeps the
    carousel cards tight and removes dead space.
    """
    bg_color = img.getpixel((0, 0))
    bg = Image.new("RGB", img.size, bg_color)
    bbox = ImageChops.difference(img.convert("RGB"), bg).getbbox()
    if not bbox:
        return img

    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(img.width, right + pad)
    bottom = min(img.height, bottom + pad)
    return img.crop((left, top, right, bottom))


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def text_width(draw, s: str, f) -> int:
    return int(draw.textbbox((0, 0), s, font=f)[2])


def pill(draw, x, y, label, f, bg, fg, pad_x=18, pad_y=9):
    w = text_width(draw, label, f)
    h = f.size + pad_y * 2
    draw.rounded_rectangle([x, y, x + w + pad_x * 2, y + h], radius=h // 2, fill=bg)
    draw.text((x + pad_x, y + pad_y - 2), label, font=f, fill=fg)
    return x + w + pad_x * 2 + 10


def build_banner() -> Path:
    """1200x627 hero banner for the README + LinkedIn link preview."""
    W, H = 1200, 627
    img = Image.new("RGB", (W, H), DARK_BG)
    d = ImageDraw.Draw(img)

    # Subtle diagonal accent wash in the top-right corner.
    for i in range(320):
        a = int(60 * (1 - i / 320))
        d.line([(W - 340 + i, 0), (W - 40 + i, 340)],
               fill=(43 + a // 3, 92 + a // 2, 184), width=1)

    d.rounded_rectangle([60, 52, 114, 106], radius=14, fill=ACCENT)
    d.text((75, 63), "B", font=font(BOLD, 34), fill="#ffffff")

    d.text((132, 54), "BlogCMS", font=font(BOLD, 34), fill="#ffffff")
    d.text((132, 96), "full-stack devops showcase", font=font(REGULAR, 17), fill="#8b949e")

    d.text((60, 178), "Shipped a production-grade", font=font(BOLD, 50), fill="#ffffff")
    d.text((60, 238), "CI/CD pipeline", font=font(BOLD, 50), fill=ACCENT)
    d.text((60, 300), "for a 3-tier blog platform.", font=font(REGULAR, 30), fill="#c9d1d9")

    # Stat chips
    x = 60
    for value, label in [("9", "tests passing"), ("3", "containers"),
                         ("4", "CI/CD gates"), ("1", "command deploy")]:
        d.rounded_rectangle([x, 380, x + 250, 468], radius=14,
                            fill=DARK_PANEL, outline="#2b313b")
        d.text((x + 26, 396), value, font=font(MONO_BOLD, 30), fill=GREEN)
        d.text((x + 26, 434), label, font=font(REGULAR, 15), fill="#8b949e")
        x += 266

    # Stack chips
    x = 60
    for label in ["React", "FastAPI", "MySQL", "Docker", "GitHub Actions", "Nginx"]:
        x = pill(d, x, 506, label, font(REGULAR, 16), "#21262d", "#c9d1d9", pad_x=16, pad_y=8)

    out = ASSETS / "banner.png"
    img.save(out)
    return out


CARDS = [
    {
        "file": "01-problem.png",
        "eyebrow": "THE PROBLEM",
        "title": "Most portfolio apps\nstop at the frontend.",
        "body": "They show a UI and a mock API.\nNo containers, no pipeline, no\nway to prove it deploys.",
        "shot": "A1-start-stack.png",
        "shot_caption": "The starting point: nothing is running",
    },
    {
        "file": "02-stack.png",
        "eyebrow": "THE STACK",
        "title": "Three tiers, three\ncontainers.",
        "body": "React + Nginx  \u00b7  FastAPI  \u00b7  MySQL 8\nWired together on a shared\nDocker bridge network.",
        "shot": "A5-docker-ps-final.png",
        "shot_caption": "docker ps \u2014 all three containers healthy",
    },
    {
        "file": "03-workflow.png",
        "eyebrow": "THE WORKFLOW",
        "title": "Real auth, real roles,\nreal content.",
        "body": "JWT login \u00b7 admin / author / reader\nDrafts stay private. Readers\nget a 403 on write.",
        "shot": "B8-post-filled.png",
        "shot_caption": "Writing and publishing through the UI",
    },
    {
        "file": "04-pipeline.png",
        "eyebrow": "THE PIPELINE",
        "title": "Tests gate the build.\nNot the other way round.",
        "body": "lint \u2192 test \u2192 build \u2192 push\nA failing test means no image\never reaches the registry.",
        "shot": "B12-swagger.png",
        "shot_caption": "Auto-generated OpenAPI docs",
    },
    {
        "file": "05-proof.png",
        "eyebrow": "THE PROOF",
        "title": "One command.\nWhole stack up.",
        "body": "docker compose up --build\nThen lint, 9 tests, and a\nproduction build all pass.",
        "shot": "B9-post-detail.png",
        "shot_caption": "The running app \u2014 end to end",
    },
]


def build_card(spec: dict, index: int, total: int) -> Path:
    """1080x1350 (4:5) LinkedIn document-post card with a screenshot window."""
    W, H = 1080, 1350
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header strip
    d.rectangle([0, 0, W, 8], fill=ACCENT)
    d.text((72, 60), "BlogCMS", font=font(BOLD, 26), fill=ACCENT_DARK)
    d.text((W - 200, 62), f"{index:02d} / {total:02d}", font=font(MONO, 20), fill=INK_SOFT)

    d.text((72, 122), spec["eyebrow"], font=font(BOLD, 20), fill=ACCENT)

    y = 166
    for line in spec["title"].split("\n"):
        d.text((72, y), line, font=font(BOLD, 50), fill=INK)
        y += 62

    y += 14
    for line in spec["body"].split("\n"):
        d.text((72, y), line, font=font(REGULAR, 25), fill=INK_SOFT)
        y += 38

    # Screenshot inside a mac-style window chrome
    shot = autocrop(Image.open(SHOTS / spec["shot"]).convert("RGB"))
    # Portrait screenshots get more vertical room so they stay legible.
    max_w, max_h = (W - 144), (640 if shot.height > shot.width else 470)
    ratio = min(max_w / shot.width, max_h / shot.height)
    shot = shot.resize((int(shot.width * ratio), int(shot.height * ratio)), Image.LANCZOS)

    win_w = shot.width + 8
    win_h = shot.height + 56
    win_x = (W - win_w) // 2

    # Centre the window in whatever space is left between the copy and footer,
    # so no card ends up with a large dead gap.
    footer_y = H - 152
    space_top = y + 34
    space_bottom = footer_y - 46
    win_top = space_top + max(0, (space_bottom - space_top - win_h) // 2)

    d.rounded_rectangle([win_x, win_top, win_x + win_w, win_top + win_h], radius=14,
                        fill=SURFACE, outline=BORDER, width=2)
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        d.ellipse([win_x + 22 + i * 26, win_top + 20,
                   win_x + 36 + i * 26, win_top + 34], fill=c)
    d.text((win_x + 112, win_top + 16), "localhost", font=font(MONO, 16), fill=INK_SOFT)
    img.paste(shot, (win_x + 4, win_top + 52))

    # Caption directly beneath the window
    d.text((72, win_top + win_h + 22), spec["shot_caption"],
           font=font(REGULAR, 21), fill=INK_SOFT)

    # Footer
    d.line([72, H - 118, W - 72, H - 118], fill=BORDER, width=2)
    d.text((72, H - 96), "docker compose up --build",
           font=font(MONO_BOLD, 22), fill=ACCENT_DARK)

    out = CAROUSEL / spec["file"]
    img.save(out)
    return out


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    CAROUSEL.mkdir(exist_ok=True)

    print("generated:", build_banner().relative_to(BASE))
    for i, spec in enumerate(CARDS, start=1):
        print("generated:", build_card(spec, i, len(CARDS)).relative_to(BASE))
    print("\nAssets written to", ASSETS)


if __name__ == "__main__":
    main()