from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.coupon import Coupon
from datetime import date

router = APIRouter(prefix="/coupons", tags=["Coupons"])

@router.post("/")
def add_coupon(code: str, discount: float, expiry: str, db: Session = Depends(get_db)):
    coupon = Coupon(code=code, discount=discount, expiry=expiry)
    db.add(coupon)
    db.commit()
    db.refresh(coupon)
    return coupon

@router.get("/")
def list_coupons(db: Session = Depends(get_db)):
    today = date.today()
    coupons = db.query(Coupon).all()
    for c in coupons:
        if c.expiry < today:
            c.status = False
    db.commit()
    return coupons
