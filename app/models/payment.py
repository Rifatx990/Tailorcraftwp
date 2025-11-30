from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database import Base

class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True)
    tran_id = Column(String(200), unique=True)
    val_id = Column(String(200))
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="SET NULL"))
    custom_order_id = Column(Integer, ForeignKey("custom_orders.id", ondelete="SET NULL"))
    amount = Column(Float)
    status = Column(String(20), default="PENDING")
    gateway = Column(String(50), default="SSLCOMMERZ")
    details = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
