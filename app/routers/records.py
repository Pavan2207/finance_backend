from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from fastapi import status

from app.database import get_db
from app.services.record_service import (
    get_records, get_record, create_record, update_record, delete_record,
    get_summary, get_recent, get_trends
)
from app.schemas.record import (
    RecordCreate, RecordUpdate, RecordOut, SummaryOut, TrendOut
)
from app.core.security import viewer_dep, analyst_dep, admin_dep, get_current_user

router = APIRouter()

@router.post("/", response_model=RecordOut, dependencies=[analyst_dep])
def create_new_record(record: RecordCreate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.user_id is None:
        raise HTTPException(status_code=400, detail="X-User-ID required for record creation")
    return create_record(db=db, record=record, user_id=current_user.user_id)

@router.get("/", response_model=List[RecordOut], dependencies=[analyst_dep])
def read_records(
    skip: int = 0, 
    limit: int = Query(100, le=200),
    type_: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    # Filter by user if analyst, all if admin
    user_id = current_user.user_id if current_user.role == 'analyst' else None
    return get_records(db, user_id, skip, limit, type_, category, start_date, end_date, search)

@router.get("/{record_id}", response_model=RecordOut, dependencies=[analyst_dep])
def read_record(record_id: int, db: Session = Depends(get_db)):
    db_record = get_record(db, record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.put("/{record_id}", response_model=RecordOut, dependencies=[admin_dep])
def record_update(record_id: int, record_update: RecordUpdate, db: Session = Depends(get_db)):
    updated = update_record(db, record_id, record_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return updated

status.HTTP_204_NO_CONTENT
def record_delete(record_id: int, db: Session = Depends(get_db)):
    deleted = delete_record(db, record_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Record not found")

@router.get("/summary/", response_model=SummaryOut)
def read_summary(db: Session = Depends(get_db)):
    return get_summary(db, None)

@router.get("/recent/", response_model=List[RecordOut])
def read_recent(limit: int = 5, db: Session = Depends(get_db)):
    return get_recent(db, None, limit)

@router.get("/trends/", response_model=List[TrendOut])
def read_trends(period: str = "monthly", db: Session = Depends(get_db)):
    return get_trends(db, None, period)
