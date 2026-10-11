# BlogCMS Demo Video Guide
Built video: `demo/BlogCMS_Demo.mp4` (1920x1080, 88s, 21 shots x 4s)

## Watch it
Double-click `demo/BlogCMS_Demo.mp4` or:
```
start demo/BlogCMS_Demo.mp4
```

## Rebuild it
```
python demo/make_video.py
```

## Voiceover (read ~1 line per 4s shot)
0 TITLE: "BlogCMS - a full-stack blog platform. React, FastAPI, MySQL, Docker, Nginx."
1 "One command starts everything - docker compose up."
2 "Three containers - database, API, frontend - all healthy."
3 "Health endpoint proves API plus database are connected."
4 "Nginx serves the frontend and proxies /api - one origin, no CORS."
5 "Fresh app - empty blog with search and category filter."
6 "Register - the first user automatically becomes admin."
7 "Signed in - header shows the admin role badge."
8 "Log out, log back in - JWT round trip works."
9 "Token persists - session restored from the API."
10 "New Post editor - protected to admin and author only."
11 "Create the DevOps category without leaving the editor."
12 "Fill title, summary, content - publish immediately."
13 "Published page on a slug URL with owner edit and delete."
14 "Comments - logged-in users post instantly."
15 "Home lists the post - search and filter pick it up."
16 "Swagger docs come free from FastAPI."
17 "Final check - containers still green."
18 "API proof - posts endpoint returns JSON."
19 "API proof - categories endpoint returns DevOps."
20 OUTRO: "Clone it, docker compose up, and it ships. Lint, test, build, then push."

## Live re-shoot checklist (if you want face-cam)
1. Start Docker Desktop, then `docker compose up --build -d`
2. Open http://localhost fullscreen (F11), zoom 100%
3. Record with Xbox Game Bar (Win+G) or OBS at 1080p
4. Follow STORY order in demo/make_video.py (19 steps)
5. Use admin/admin@example.com/admin12345 demo account
6. End on http://localhost:8000/docs for Swagger money-shot
