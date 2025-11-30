from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
import os, shutil
from app.database import get_db
from app.models.product import Product, Category

router = APIRouter(prefix="/products", tags=["Products"])
UPLOAD_DIR = "app/uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def add_product(
    name: str = Form(...),
    price: float = Form(...),
    stock: int = Form(...),
    category_id: int = Form(...),
    description: str = Form(None),
    images: list[UploadFile] = File([]),
    db: Session = Depends(get_db)
):
    saved_images = []
    for img in images:
        path = os.path.join(UPLOAD_DIR, img.filename)
        with open(path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
        saved_images.append(img.filename)

    product = Product(
        name=name, price=price, stock=stock,
        category_id=category_id, description=description,
        images=",".join(saved_images)
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
