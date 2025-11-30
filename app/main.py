from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import (
    auth, products, orders, custom_orders, payments,
    workers, coupons, banners, reports, admin
)

# ----------------------------
# Initialize Database
# ----------------------------
Base.metadata.create_all(bind=engine)

# ----------------------------
# Initialize FastAPI App
# ----------------------------
app = FastAPI(
    title="TailorCraft Ultra-Pro Enterprise API",
    description="Full-featured E-commerce & Tailoring Management API",
    version="1.0.0"
)

# ----------------------------
# CORS Middleware (optional)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Include Routers
# ----------------------------
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(custom_orders.router)
app.include_router(payments.router)
app.include_router(workers.router)
app.include_router(coupons.router)
app.include_router(banners.router)
app.include_router(reports.router)
app.include_router(admin.router)

# ----------------------------
# Health Check
# ----------------------------
@app.get("/")
def home():
    return {"message": "TailorCraft Ultra-Pro Enterprise API is running ✅"}

# ----------------------------
# Optional startup event
# ----------------------------
@app.on_event("startup")
def startup_event():
    print("🚀 TailorCraft API started and ready to serve requests")
