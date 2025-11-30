from fastapi import APIRouter, Request, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.payment import Payment
from app.models.order import Order
from app.models.custom_order import CustomOrder
from app.models.auth import Customer
from app.utils.tasks import send_order_confirmation_email, send_custom_order_notification

router = APIRouter(prefix="/payments", tags=["Payments"])

# ----------------------------
# Payment Success
# ----------------------------
@router.post("/success")
async def payment_success(
    request: Request,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    form = await request.form()
    tran_id = form.get("tran_id")
    val_id = form.get("val_id")
    status = form.get("status", "SUCCESS")

    payment = db.query(Payment).filter(Payment.tran_id == tran_id).first()
    if payment:
        payment.status = status
        payment.val_id = val_id
        db.commit()
        db.refresh(payment)

        # Update associated order or custom order
        if payment.order_id:
            order = db.query(Order).filter(Order.id == payment.order_id).first()
            if order:
                order.payment_status = "PAID"
                db.commit()
                # Send email to customer
                customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
                if customer:
                    send_order_confirmation_email(background_tasks, customer.email, order.id)

        elif payment.custom_order_id:
            custom_order = db.query(CustomOrder).filter(CustomOrder.id == payment.custom_order_id).first()
            if custom_order:
                custom_order.status = "PAID"
                db.commit()
                customer = db.query(Customer).filter(Customer.id == custom_order.customer_id).first()
                if customer:
                    send_custom_order_notification(background_tasks, customer.email, custom_order.id)

    return {"message": "Payment successful", "tran_id": tran_id, "status": status}


# ----------------------------
# Payment Fail
# ----------------------------
@router.post("/fail")
async def payment_fail(
    request: Request,
    db: Session = Depends(get_db)
):
    form = await request.form()
    tran_id = form.get("tran_id")
    status = form.get("status", "FAILED")

    payment = db.query(Payment).filter(Payment.tran_id == tran_id).first()
    if payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
    return {"message": "Payment failed", "tran_id": tran_id, "status": status}


# ----------------------------
# Payment Cancel
# ----------------------------
@router.post("/cancel")
async def payment_cancel(
    request: Request,
    db: Session = Depends(get_db)
):
    form = await request.form()
    tran_id = form.get("tran_id")
    status = form.get("status", "CANCELLED")

    payment = db.query(Payment).filter(Payment.tran_id == tran_id).first()
    if payment:
        payment.status = status
        db.commit()
        db.refresh(payment)
    return {"message": "Payment cancelled", "tran_id": tran_id, "status": status}
