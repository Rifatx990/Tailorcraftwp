from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem
from app.utils.helpers import calculate_order_total

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(customer_id: int, items: list, payment_method: str, db: Session = Depends(get_db)):
    total = calculate_order_total(items)
    order = Order(customer_id=customer_id, total_amount=total, payment_method=payment_method)
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in items:
        db.add(OrderItem(order_id=order.id, product_id=item['product_id'], price=item['price'], qty=item['qty']))
    db.commit()
    return order

@router.get("/")
def list_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()
