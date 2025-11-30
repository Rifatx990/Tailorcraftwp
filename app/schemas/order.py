from pydantic import BaseModel
from typing import List, Optional

# ----------------------------
# Order Schemas
# ----------------------------
class OrderItemSchema(BaseModel):
    product_id: int
    price: float
    qty: int

class OrderCreateSchema(BaseModel):
    customer_id: int
    items: List[OrderItemSchema]
    payment_method: str  # 'COD' or 'online'

class OrderResponseSchema(BaseModel):
    id: int
    customer_id: int
    total_amount: float
    status: str
    payment_status: str
    payment_method: str

    class Config:
        orm_mode = True

class CustomOrderMeasurement(BaseModel):
    part: str
    value: float

class CustomOrderCreate(BaseModel):
    customer_id: int
    clothing_type: str
    delivery_date: str
    urgency_level: str
    measurements: List[CustomOrderMeasurement]
