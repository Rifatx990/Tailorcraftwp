from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.worker import Worker, WorkerTask, CustomOrder

router = APIRouter(prefix="/workers", tags=["Workers"])

@router.post("/")
def add_worker(name: str, phone: str, role: str, salary_type: str, password: str, db: Session = Depends(get_db)):
    from app.utils.security import hash_password
    worker = Worker(name=name, phone=phone, role=role, salary_type=salary_type, password=hash_password(password))
    db.add(worker)
    db.commit()
    db.refresh(worker)
    return worker

@router.get("/")
def list_workers(db: Session = Depends(get_db)):
    return db.query(Worker).all()

@router.post("/assign_task")
def assign_task(worker_id: int, custom_order_id: int, db: Session = Depends(get_db)):
    task = WorkerTask(worker_id=worker_id, order_id=custom_order_id, status="Pending")
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/tasks/{worker_id}")
def worker_tasks(worker_id: int, db: Session = Depends(get_db)):
    return db.query(WorkerTask).filter(WorkerTask.worker_id == worker_id).all()
