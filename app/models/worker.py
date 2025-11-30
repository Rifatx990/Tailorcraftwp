from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class WorkerPayment(Base):
    __tablename__ = "worker_payments"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id"))
    amount = Column(Float)
    payment_type = Column(String(50))  # Salary / Piece rate
    date = Column(DateTime, default=func.now())
