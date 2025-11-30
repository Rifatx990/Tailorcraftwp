from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.custom_order import CustomOrder, Measurement, WorkerTask
import os, shutil

router = APIRouter(prefix="/custom_orders", tags=["Custom Orders"])
UPLOAD_DIR = "app/uploads/custom_orders"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def create_custom_order(
    customer_id: int = Form(...),
    clothing_type: str = Form(...),
    delivery_date: str = Form(...),
    urgency_level: str = Form(...),
    design: UploadFile = File(...),
    measurements: str = Form(...),
    db: Session = Depends(get_db)
):
    # Save design image
    path = os.path.join(UPLOAD_DIR, design.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(design.file, buffer)

    order = CustomOrder(
        customer_id=customer_id,
        clothing_type=clothing_type,
        delivery_date=delivery_date,
        urgency_level=urgency_level,
        design_image=design.filename
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # Save measurements (JSON string expected)
    import json
    measurements = json.loads(measurements)
    for m in measurements:
        db.add(Measurement(order_id=order.id, part=m["part"], value=m["value"]))
    db.commit()

    return {"order_id": order.id, "status": "pending"}
