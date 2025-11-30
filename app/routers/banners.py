from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.banner import Banner
import os, shutil

router = APIRouter(prefix="/banners", tags=["Banners"])
UPLOAD_DIR = "app/uploads/banners"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def add_banner(image: UploadFile = File(...), link: str = Form(None), db: Session = Depends(get_db)):
    path = os.path.join(UPLOAD_DIR, image.filename)
    with open(path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    banner = Banner(image=image.filename, link=link)
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner

@router.get("/")
def list_banners(db: Session = Depends(get_db)):
    return db.query(Banner).filter(Banner.status == True).all()
