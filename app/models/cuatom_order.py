from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.sql import func

class CustomOrder(Base):
    __tablename__ = "custom_orders"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    clothing_type = Column(String(100))
    delivery_date = Column(Date)
    urgency_level = Column(String(20))
    design_image = Column(String(500))
    status = Column(String(50), default="Pending")
    created_at = Column(DateTime, server_default=func.now())

class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("custom_orders.id", ondelete="CASCADE"))
    part = Column(String(50))
    value = Column(Float)

class WorkerTask(Base):
    __tablename__ = "worker_tasks"
    id = Column(Integer, primary_key=True)
    worker_id = Column(Integer, ForeignKey("workers.id", ondelete="CASCADE"))
    order_id = Column(Integer, ForeignKey("custom_orders.id", ondelete="CASCADE"))
    status = Column(String(50), default="Pending")
