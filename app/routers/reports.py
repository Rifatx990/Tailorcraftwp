from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.worker import WorkerTask, Worker
from datetime import datetime, timedelta

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/sales")
def sales_report(period: str = "daily", db: Session = Depends(get_db)):
    now = datetime.now()
    query = db.query(Order)
    if period == "daily":
        query = query.filter(Order.created_at >= now - timedelta(days=1))
    elif period == "monthly":
        query = query.filter(Order.created_at >= now - timedelta(days=30))
    elif period == "yearly":
        query = query.filter(Order.created_at >= now - timedelta(days=365))
    total = sum(o.total_amount for o in query.all())
    return {"period": period, "total_sales": total}

@router.get("/worker_payments")
def worker_payment_report(db: Session = Depends(get_db)):
    workers = db.query(Worker).all()
    report = []
    for w in workers:
        tasks = db.query(WorkerTask).filter(WorkerTask.worker_id == w.id).all()
        report.append({
            "worker_id": w.id,
            "worker_name": w.name,
            "tasks_completed": len([t for t in tasks if t.status == "Completed"])
        })
    return report
