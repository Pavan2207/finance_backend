from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.sql import func as sqlfunc
from datetime import date, timedelta
from typing import List, Optional

from app.models.record import Record
from app.schemas.record import RecordCreate, RecordUpdate, SummaryOut, TrendOut

def get_records(db: Session, user_id: Optional[int] = None, skip: int = 0, limit: int = 100, type_: Optional[str] = None, category: Optional[str] = None, search: Optional[str] = None, start_date: Optional[date] = None, end_date: Optional[date] = None):
    stmt = select(Record).where(Record.deleted_at.is_(None)).offset(skip).limit(limit)
    if user_id:
        stmt = stmt.where(Record.user_id == user_id)
    if type_:
        stmt = stmt.where(Record.type == type_)
    if category:
        stmt = stmt.where(Record.category.ilike(f"%{category}%"))
    if search:
        stmt = stmt.where(Record.notes.ilike(f"%{search}%"))
    if start_date:
        stmt = stmt.where(Record.date >= start_date)
    if end_date:
        stmt = stmt.where(Record.date <= end_date)
    stmt = stmt.order_by(Record.date.desc())
    return db.execute(stmt).scalars().all()

def get_record(db: Session, record_id: int):
    return db.execute(select(Record).where(Record.id == record_id, Record.deleted_at.is_(None))).scalar_one_or_none()

def get_user_records(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    stmt = select(Record).where(Record.user_id == user_id, Record.deleted_at.is_(None)).offset(skip).limit(limit).order_by(Record.date.desc())
    return db.execute(stmt).scalars().all()

def create_record(db: Session, record: RecordCreate, user_id: int):
    db_record = Record(**record.model_dump(), user_id=user_id)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_record(db: Session, record_id: int, record_update: RecordUpdate):
    stmt = update(Record).where(Record.id == record_id, Record.deleted_at.is_(None)).values(**record_update.model_dump(exclude_unset=True)).returning(Record)
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()

def delete_record(db: Session, record_id: int):
    stmt = update(Record).where(Record.id == record_id).values(deleted_at=func.now()).returning(Record)
    result = db.execute(stmt)
    db.commit()
    return result.scalar_one_or_none()

def get_summary(db: Session, user_id: Optional[int] = None) -> SummaryOut:
    filters = []
    if user_id:
        filters.append(Record.user_id == user_id)
    
    total_income = db.execute(
        select(func.sum(Record.amount)).where(and_(*(filters + [Record.type == 'income', Record.deleted_at.is_(None)])))
    ).scalar() or 0
    
    total_expense = db.execute(
        select(func.sum(Record.amount)).where(and_(*(filters + [Record.type == 'expense', Record.deleted_at.is_(None)])))
    ).scalar() or 0
    
    income_by_cat = db.execute(
        select(Record.category, func.sum(Record.amount))
        .where(and_(*(filters + [Record.type == 'income', Record.deleted_at.is_(None)])))
        .group_by(Record.category)
    ).all()
    
    cat_totals = {cat: float(amt) for cat, amt in income_by_cat}
    
    return SummaryOut(
        total_income=float(total_income),
        total_expense=float(total_expense),
        net_balance=float(total_income - total_expense),
        category_totals=cat_totals
    )

def get_recent(db: Session, user_id: Optional[int] = None, limit: int = 5) -> List[Record]:
    stmt = select(Record).where(Record.deleted_at.is_(None)).order_by(Record.created_at.desc()).limit(limit)
    if user_id:
        stmt = stmt.where(Record.user_id == user_id)
    return db.execute(stmt).scalars().all()

def get_trends(db: Session, user_id: Optional[int] = None, period: str = 'monthly') -> List[TrendOut]:
    trends = []
    end = date.today()
    if period == 'monthly':
        start = end.replace(day=1) - timedelta(days=365)
        stmt = select(
            func.to_char(Record.date, 'YYYY-MM').label('period'),
            sqlfunc.sum(Record.amount).filter(Record.type == 'income').label('income'),
            sqlfunc.sum(Record.amount).filter(Record.type == 'expense').label('expense')
        ).where(
            and_(
                Record.date >= start,
                Record.date <= end,
                Record.deleted_at.is_(None),
                *(Record.user_id == user_id,)
            )
        ).group_by('period').order_by('period')
        results = db.execute(stmt).all()
        for per, inc, exp in results:
            trends.append(TrendOut(period=str(per), income=float(inc or 0), expense=float(exp or 0), net=float((inc or 0) - (exp or 0))))
    return trends

