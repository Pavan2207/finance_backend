from sqlalchemy import Column, Integer, Float, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # income, expense
    category = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String)

    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)
