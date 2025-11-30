from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.auth import Customer

router = APIRouter(prefix="/customers", tags=["Customers"])

@router.get("/")
def list_customers(db: Session = Depends(get_db)):
    return db.query(Customer).all()

@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    return customer
