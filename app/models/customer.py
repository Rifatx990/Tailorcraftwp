from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.sql import func
from app.database import Base

class CustomerMeasurement(Base):
    __tablename__ = "customer_measurements"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    measurement_data = Column(JSON)  # JSON for shirt/pant/etc measurements
    created_at = Column(DateTime, server_default=func.now())
