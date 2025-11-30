from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.payment import Payment
from app.sslcommerz import create_payment_session, validate_payment

router = APIRouter(prefix="/payment", tags=["Payments"])

def process_payment(db: Session, amount, customer_id, order_id=None, custom_order_id=None):
    response = create_payment_session(amount, "Customer", "email@test.com", "0170000000")
    payment = Payment(
        tran_id=response["tran_id"], amount=amount, status="PENDING",
        order_id=order_id, custom_order_id=custom_order_id
    )
    db.add(payment)
    db.commit()
    return response["GatewayPageURL"]

@router.post("/success")
async def payment_success(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    val_id = form.get("val_id")
    tran_id = form.get("tran_id")
    validation = validate_payment(val_id)
    payment = db.query(Payment).filter_by(tran_id=tran_id).first()
    if payment:
        payment.status = "SUCCESS"
        payment.details = str(validation)
        db.commit()
    return {"status": "success", "data": validation}
