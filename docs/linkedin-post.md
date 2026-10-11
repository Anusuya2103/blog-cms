# LinkedIn post — ready to publish

Everything you need to ship this project to LinkedIn. Copy the text below,
attach the images listed at the bottom, and post.

---

## Option A — Document post (recommended)

Upload these five images **in this exact order** — LinkedIn renders a
document carousel and it gets far more reach than a single image:

1. `assets/carousel/01-problem.png`
2. `assets/carousel/02-stack.png`
3. `assets/carousel/03-workflow.png`
4. `assets/carousel/04-pipeline.png`
5. `assets/carousel/05-proof.png`

Then use this caption:

---

> Most portfolio projects stop at "it runs on localhost."
>
> I wanted to build the thing that comes *after* that — the part that decides
> whether a project could actually ship, and whether you'd know if it broke.
>
> So I built **BlogCMS**: a 3-tier blog platform where the DevOps pipeline,
> not the CRUD, is the real deliverable.
>
> **The stack**
> React (Vite) · FastAPI · MySQL 8 · Docker Compose · GitHub Actions · Nginx
>
> **What actually works**
> → JWT auth with real role enforcement (admin / author / reader)
> → Draft posts stay private; a `reader` gets a 403 on write
> → bcrypt password hashing, pre-hashed so long passphrases aren't silently truncated
> → `docker compose up --build` brings up MySQL + API + frontend together
> → 9 automated tests, green, no external services needed
>
> **The part I'm most proud of**
>
> The CI pipeline runs `lint → test → build → push`. Docker images are only
> built *after* lint, tests, and the production build have all passed.
>
> That ordering is the whole point. A broken change can't reach the registry,
> let alone production.
>
> Most of what I learned here wasn't in any tutorial:
> → `passlib` is unmaintained and breaks against `bcrypt >= 5.x`. I found out
>   because 3 tests failed on a fresh clone even though CI was green.
> → bcrypt ignores everything past 72 bytes, so I SHA-256 pre-hash first —
>   otherwise two long passphrases sharing a prefix collide.
> → Pin your dependencies, or your CI proves nothing about a real clone.
>
> Full architecture, docs, and setup in the repo.
> Repo link in the comments 👇
>
> What did you get wrong on your last project that a test would have caught?
>
> \#DevOps \#Docker \#FastAPI \#React \#GitHubActions \#CI/CD \#CloudNative \#Python

---

## Option B — Single image post

Use one image: `assets/banner.png` (1200×627 — the exact aspect ratio
LinkedIn renders best for link previews).

Caption:

---

> I built BlogCMS — a 3-tier blog platform where the DevOps pipeline, not the
> CRUD, is the real deliverable.
>
> React · FastAPI · MySQL · Docker · GitHub Actions · Nginx
>
> Every service is containerized. Images are only built after lint, tests, and
> the production build pass. `docker compose up --build` brings the whole
> stack up in one command.
>
> The bug that taught me the most: `passlib` is unmaintained and breaks
> against `bcrypt >= 5.x`. My CI was green, but a fresh clone failed 3 tests.
> Green CI that doesn't match a real clone isn't green — it's just untested.
>
> Repo link in the comments 👇
>
> \#DevOps \#Docker \#FastAPI \#React \#GitHubActions \#CI/CD \#Python

---

## Notes

- **Replace `OWNER`** in the README badges and clone URL with your GitHub
  username before publishing (search the repo for `OWNER`).
- Put the repo link in the **first comment**, not the post body — LinkedIn
  suppresses reach on posts with outbound links in the text.
- Post Tuesday–Thursday, 8–10am in your audience's timezone.
- The most engagement comes from the closing question. Keep it.
- Regenerate assets any time with `python demo/make_showcase.py` (requires
  `pip install pillow`).

## Regenerating the assets

```bash
pip install pillow
python demo/make_showcase.py
```

Rebuilds `assets/banner.png` and all five carousel cards from the screenshots
in `demo/shots/`. If you change the copy in `CARDS` at the top of the script,
re-run it and the carousel updates automatically.