import re
import time
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/posts", tags=["Posts"])


def slugify(title: str) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    return f"{base}-{int(time.time())}"


@router.get("", response_model=list[schemas.PostListOut])
def list_posts(
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    search: Optional[str] = None,
    published_only: bool = True,
    skip: int = 0,
    limit: int = Query(default=20, le=100),
):
    q = db.query(models.Post)
    if published_only:
        q = q.filter(models.Post.published == 1)
    if category:
        q = q.join(models.Post.categories).filter(models.Category.slug == category)
    if search:
        like = f"%{search}%"
        q = q.filter(models.Post.title.ilike(like) | models.Post.content.ilike(like))
    return q.order_by(models.Post.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{slug}", response_model=schemas.PostOut)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.slug == slug).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("", response_model=schemas.PostOut, status_code=201)
def create_post(
    payload: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(models.RoleEnum.admin, models.RoleEnum.author)),
):
    categories = []
    if payload.category_ids:
        categories = db.query(models.Category).filter(models.Category.id.in_(payload.category_ids)).all()

    post = models.Post(
        title=payload.title,
        slug=slugify(payload.title),
        content=payload.content,
        summary=payload.summary,
        published=1 if payload.published else 0,
        author_id=current_user.id,
        categories=categories,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=schemas.PostOut)
def update_post(
    post_id: int,
    payload: schemas.PostUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed to edit this post")

    if payload.title is not None:
        post.title = payload.title
    if payload.content is not None:
        post.content = payload.content
    if payload.summary is not None:
        post.summary = payload.summary
    if payload.published is not None:
        post.published = 1 if payload.published else 0
    if payload.category_ids is not None:
        post.categories = db.query(models.Category).filter(
            models.Category.id.in_(payload.category_ids)
        ).all()

    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id and current_user.role != models.RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")

    db.delete(post)
    db.commit()
