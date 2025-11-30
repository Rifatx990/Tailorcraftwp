from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# Product Schemas
# ----------------------------
class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category_id: int
    description: Optional[str] = None

class ProductCreate(ProductBase):
    images: Optional[List[str]] = []

class ProductResponse(ProductBase):
    id: int
    images: Optional[List[str]] = []

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str
    image: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        orm_mode = True
