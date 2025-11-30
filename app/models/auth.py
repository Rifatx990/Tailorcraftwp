from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="admin")
    created_at = Column(DateTime, server_default=func.now())

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    phone = Column(String(50))
    password = Column(String(255), nullable=False)
    role = Column(String(50), default="customer")
    created_at = Column(DateTime, server_default=func.now())

class Worker(Base):
    __tablename__ = "workers"
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(50))
    role = Column(String(50))
    salary_type = Column(String(20))  # monthly / piece_rate
    password = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
