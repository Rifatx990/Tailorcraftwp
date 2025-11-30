from fastapi import APIRouter, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.payment import Payment
from app.utils.security import create_access_token
from app.config import settings
import requests

router = APIRouter(prefix="/payments", tags=["Payments"])

SSLCZ_API = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"

@router.post("/initiate")
def initiate_payment(order_id: int = None, custom_order_id: int = None, amount: float = 0.0, db: Session = Depends(get_db)):
    data = {
        "store_id": settings.SSLCZ_STORE_ID,
        "store_passwd": settings.SSLCZ_STORE_PASS,
        "total_amount": amount,
        "currency": "BDT",
        "tran_id": f"TC-{order_id or custom_order_id}-{int(amount*1000)}",
        "success_url": f"{settings.BASE_URL}/payments/success",
        "fail_url": f"{settings.BASE_URL}/payments/fail",
        "cancel_url": f"{settings.BASE_URL}/payments/cancel",
        "emi_option": 0
    }
    response = requests.post(SSLCZ_API, data=data)
    return response.json()

@router.post("/ipn")
def sslcommerz_ipn(tran_id: str, val_id: str, status: str, db: Session = Depends(get_db)):
    payment = Payment(tran_id=tran_id, val_id=val_id, amount=0, status=status)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return {"message": "IPN received"}
