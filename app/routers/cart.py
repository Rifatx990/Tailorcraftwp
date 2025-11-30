from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import OrderItem
from app.models.auth import Customer

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/add")
def add_to_cart(customer_id: int, product_id: int, qty: int = 1, db: Session = Depends(get_db)):
    item = OrderItem(customer_id=customer_id, product_id=product_id, qty=qty, price=0)  # Price filled on checkout
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
