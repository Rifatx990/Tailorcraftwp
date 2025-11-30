from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database import get_db
from app.models.auth import Admin, Customer, Worker
from app.utils.security import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Admin).filter(Admin.username == form_data.username).first() \
           or db.query(Customer).filter(Customer.email == form_data.username).first() \
           or db.query(Worker).filter(Worker.phone == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/register/customer")
def register_customer(name: str, email: str, phone: str, password: str, db: Session = Depends(get_db)):
    hashed = hash_password(password)
    customer = Customer(name=name, email=email, phone=phone, password=hashed)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return {"id": customer.id, "email": customer.email, "name": customer.name}
