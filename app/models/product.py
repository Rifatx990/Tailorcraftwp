from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from app.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    image = Column(String(500))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL"))
    price = Column(Float)
    stock = Column(Integer)
    description = Column(Text)
    images = Column(Text)  # Comma-separated filenames
