from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.auth import Admin, Customer, Worker
from app.utils.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

# ----------------------------
# Customer Registration
# ----------------------------
@router.post("/register")
def register_customer(name: str, email: str, phone: str, password: str, db: Session = Depends(get_db)):
    existing = db.query(Customer).filter(Customer.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    customer = Customer(name=name, email=email, phone=phone, password=hash_password(password))
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return {"message": "Customer registered successfully", "customer_id": customer.id}

# ----------------------------
# Login (Customer/Admin/Worker)
# ----------------------------
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Try customer first
    user = db.query(Customer).filter(Customer.email == form_data.username).first()
    if not user:
        user = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not user:
        user = db.query(Worker).filter(Worker.name == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"user_id": user.id, "role": getattr(user, "role", "customer")})
    return {"access_token": token, "token_type": "bearer"}
