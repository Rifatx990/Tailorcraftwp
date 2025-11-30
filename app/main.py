from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, products, orders, custom_orders, payments

Base.metadata.create_all(bind=engine)

app = FastAPI(title="TailorCraft – Ultra-Pro API")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(custom_orders.router)
app.include_router(payments.router)

@app.get("/")
def home():
    return {"message": "TailorCraft Ultra-Pro API Running"}
