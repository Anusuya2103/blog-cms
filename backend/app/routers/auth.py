from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas, auth

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        (models.User.username == payload.username) | (models.User.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # First registered user becomes admin; rest default to reader
    is_first_user = db.query(models.User).count() == 0
    user = models.User(
        username=payload.username,
        email=payload.email,
        hashed_password=auth.get_password_hash(payload.password),
        role=models.RoleEnum.admin if is_first_user else models.RoleEnum.reader,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=schemas.Token)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == payload.username).first()
    if not user or not auth.verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = auth.create_access_token(data={"sub": user.username})
    return schemas.Token(access_token=token, user=user)


@router.get("/me", response_model=schemas.UserOut)
def read_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user


@router.post("/promote/{user_id}", response_model=schemas.UserOut)
def promote_to_author(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role(models.RoleEnum.admin)),
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.role = models.RoleEnum.author
    db.commit()
    db.refresh(user)
    return user
