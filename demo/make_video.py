#!/usr/bin/env python3
"""BlogCMS demo video builder: shots -> 1080p MP4 slideshow."""
from pathlib import Path
import subprocess, sys
from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent.parent
SHOTS = BASE / "demo" / "shots"
FRAMES = BASE / "demo" / "video_frames"
OUT = BASE / "demo" / "BlogCMS_Demo.mp4"
W, H, CAP_H = 1920, 1080, 150
FONT_DIR = Path("C:/Windows/Fonts")

STORY = [
    ("TITLE", "BlogCMS - full-stack blog platform", "React - FastAPI - MySQL - Docker - Nginx"),
    ("A1-start-stack.png", "1 - One command starts everything", "docker compose up --build -d"),
    ("A2-docker-ps.png", "2 - Three containers, all healthy", "db - backend - frontend on blog-net"),
    ("A3-backend-health.png", "3 - API health check", "GET /api/health -> ok + connected"),
    ("A4-proxy-health.png", "4 - One origin, no CORS pain", "Nginx proxies /api/* to backend"),
    ("B1-home-empty.png", "5 - Fresh app, empty blog", "localhost - search + filter ready"),
    ("B2-register-filled.png", "6 - Register becomes admin", "First user auto-becomes admin"),
    ("B3-home-admin.png", "7 - Signed in + role badge", "Header shows username + admin tag"),
    ("B4-login-filled.png", "8 - Logout then login", "JWT round-trip through the UI"),
    ("B5-home-login.png", "9 - Logged in again", "Token persists via /api/auth/me"),
    ("B6-new-post.png", "10 - Editor is protected", "Only admin / author reach /new-post"),
    ("B7-category-added.png", "11 - Categories inline", "Create DevOps without leaving editor"),
    ("B8-post-filled.png", "12 - Write + publish", "Title, summary, draft-vs-publish"),
    ("B9-post-detail.png", "13 - Published page", "Slug URL + owner edit/delete"),
    ("B10-comment.png", "14 - Comments", "Logged-in users comment instantly"),
    ("B11-home-post.png", "15 - Home lists the post", "Search + filter pick it up"),
    ("B12-swagger.png", "16 - Swagger docs free", "OpenAPI UI at :8000/docs"),
    ("A5-docker-ps-final.png", "17 - Still green", "Final docker ps all healthy"),
    ("A6-posts-api.png", "18 - API proof: posts", "GET /api/posts returns demo post"),
    ("A7-categories-api.png", "19 - API proof: categories", "GET /api/categories -> DevOps"),
    ("OUTRO", "docker compose up --build", "Lint - test - build - push - deploy"),
]
def F(p, s):
    try:
        return ImageFont.truetype(str(p), s)
    except Exception:
        return ImageFont.load_default()

def fit(img, bw, bh):
    img = img.convert("RGB")
    img.thumbnail((bw, bh), Image.LANCZOS)
    c = Image.new("RGB", (bw, bh), (15, 18, 24))
    c.paste(img, ((bw - img.width)//2, (bh - img.height)//2))
    return c

def card(title, sub):
    img = Image.new("RGB", (W, H), (15, 18, 24))
    d = ImageDraw.Draw(img)
    d.text((W//2-560, 400), title, font=F(FONT_DIR/"arialbd.ttf", 76), fill=(230,237,243))
    d.text((W//2-560, 520), sub, font=F(FONT_DIR/"arial.ttf", 38), fill=(125,211,252))
    d.text((W//2-280, 950), "BlogCMS - React - FastAPI - MySQL - Docker", font=F(FONT_DIR/"arial.ttf", 26), fill=(139,147,165))
    return img

def shot_frame(path, title, sub):
    top = fit(Image.open(path), W, H - CAP_H)
    c = Image.new("RGB", (W, H), (15, 18, 24))
    c.paste(top, (0, 0))
    d = ImageDraw.Draw(c)
    d.rectangle([0, H-CAP_H, W, H], fill=(23,27,35))
    d.text((60, H-CAP_H+20), title, font=F(FONT_DIR/"arialbd.ttf", 46), fill=(230,237,243))
    d.text((60, H-54), sub, font=F(FONT_DIR/"arial.ttf", 28), fill=(157,166,181))
    return c

def main():
    FRAMES.mkdir(exist_ok=True)
    for p in FRAMES.glob("*.png"):
        p.unlink()
    outs = []
    for i, (name, title, sub) in enumerate(STORY):
        src = SHOTS / name
        img = card(title, sub) if name in ("TITLE","OUTRO") else (shot_frame(src, title, sub) if src.exists() else None)
        if img is None:
            print("  [skip] missing", name); continue
        o = FRAMES / f"{i:02d}.png"
        img.save(o); outs.append(o); print("  frame", o.name, "<-", name)
    lst = FRAMES / "concat.txt"
    with open(lst, "w") as f:
        [f.write(f"file '{p.as_posix()}'\nduration 4\n") for p in outs]
        f.write(f"file '{outs[-1].as_posix()}'\n")
    r = subprocess.run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),"-vf","scale=1920:1080,format=yuv420p","-r","30","-c:v","libx264","-crf","20",str(OUT)], capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-2000:]); return 1
    print(f">> OK {OUT} {OUT.stat().st_size/1e6:.1f}MB {len(outs)}x4s=~{len(outs)*4}s")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

