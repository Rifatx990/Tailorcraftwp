from sqlalchemy import Column, Integer, String, Float, Date, Boolean
from app.database import Base

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True)
    code = Column(String(50), unique=True)
    discount = Column(Float)
    expiry = Column(Date)
    status = Column(Boolean, default=True)
