from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.logs import ActivityLog

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/log_action")
def log_action(admin_id: int, action: str, db: Session = Depends(get_db)):
    log = ActivityLog(admin_id=admin_id, action=action)
    db.add(log)
    db.commit()
    return log

@router.get("/logs")
def list_logs(db: Session = Depends(get_db)):
    return db.query(ActivityLog).order_by(ActivityLog.created_at.desc()).all()
