from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from app.schemas.user import UserOut

class RecordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    amount: float
    type: str  # income, expense
    category: str
    date: date
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    amount: Optional[float] = None
    type: Optional[str] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

class RecordOut(RecordBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: Optional[datetime]
    deleted_at: Optional[datetime] = None

class SummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    total_income: float
    total_expense: float
    net_balance: float
    category_totals: dict[str, float]

class TrendOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    period: str
    income: float
    expense: float
    net: float

class TrendsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    trends: List[TrendOut]
