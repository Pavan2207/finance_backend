from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate

def get_users(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(User).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_user(db: Session, user_id: int):
    return db.get(User, user_id)

def get_user_by_email(db: Session, email: str):
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    stmt = update(User).where(User.id == user_id).values(**user_update.model_dump(exclude_unset=True)).returning(User)
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()

def delete_user(db: Session, user_id: int):
    stmt = delete(User).where(User.id == user_id).returning(User)
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()

