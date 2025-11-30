from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem
from app.routers.payments import process_payment

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/create")
def create_order(customer_id: int, items: list, payment_method: str, db: Session = Depends(get_db)):
    total = sum(item["price"] * item["qty"] for item in items)
    order = Order(customer_id=customer_id, total_amount=total, payment_method=payment_method)
    db.add(order)
    db.commit()
    db.refresh(order)

    for i in items:
        db.add(OrderItem(order_id=order.id, product_id=i["product_id"], price=i["price"], qty=i["qty"]))
    db.commit()

    if payment_method == "online":
        url = process_payment(db, total, customer_id, order_id=order.id)
        return {"order_id": order.id, "payment_url": url}

    return {"order_id": order.id, "status": "pending"}
