from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.custom_order import CustomOrder, Measurement

router = APIRouter(prefix="/custom_orders", tags=["Custom Orders"])

@router.post("/")
def create_custom_order(customer_id: int, clothing_type: str, delivery_date: str, urgency_level: str, measurements: list, db: Session = Depends(get_db)):
    order = CustomOrder(customer_id=customer_id, clothing_type=clothing_type, delivery_date=delivery_date, urgency_level=urgency_level)
    db.add(order)
    db.commit()
    db.refresh(order)
    for m in measurements:
        db.add(Measurement(order_id=order.id, part=m['part'], value=m['value']))
    db.commit()
    return order

@router.get("/")
def list_custom_orders(db: Session = Depends(get_db)):
    return db.query(CustomOrder).all()
