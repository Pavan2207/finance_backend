from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.services.user_service import get_users, get_user_by_email, create_user, update_user, delete_user, get_user
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.core.security import admin_dep

router = APIRouter()

@router.post("/", response_model=UserOut, dependencies=[admin_dep])
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)

@router.get("/", response_model=List[UserOut], dependencies=[admin_dep])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_users(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=UserOut, dependencies=[admin_dep])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/{user_id}", response_model=UserOut, dependencies=[admin_dep])
def user_update(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    updated = update_user(db, user_id, user_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[admin_dep])
def user_delete(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user(db, user_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
