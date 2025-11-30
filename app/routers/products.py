from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product, Category

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def add_product(name: str, price: float, stock: int, category_id: int, description: str = None, db: Session = Depends(get_db)):
    product = Product(name=name, price=price, stock=stock, category_id=category_id, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
