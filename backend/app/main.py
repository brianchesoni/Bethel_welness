from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import init_db, SessionLocal
from app.routes import preorders, products  # <- updated import
from app.models import Product

app = FastAPI(title="Bethel Wellness API")

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API Routers
# -----------------------------
app.include_router(preorders.router, prefix="/api")   # POST /api/preorders
app.include_router(products.router, prefix="/api")    # GET /api/products

# -----------------------------
# Serve frontend
# -----------------------------
app.mount("/", StaticFiles(directory="app/frontend_dist", html=True), name="frontend")

# -----------------------------
# Populate default products
# -----------------------------
def populate_products():
    db: Session = SessionLocal()
    try:
        if db.query(Product).count() == 0:
            default_products = [
                {"name": "Super Collagen Plus", "description": "Supports skin, hair, nails & joints", "price": 2500},
                {"name": "Vitamin C Complex", "description": "Boosts immunity and energy", "price": 1500},
                {"name": "Biotin Hair Boost", "description": "Healthy hair & nails", "price": 1800},
            ]
            for p in default_products:
                db.add(Product(**p))
            db.commit()
            print("Default products populated!")
    finally:
        db.close()

# -----------------------------
# Startup
# -----------------------------
@app.on_event("startup")
def on_startup():
    print("Starting Bethel Wellness API...")
    init_db()
    populate_products()
    print("Startup complete.")

# -----------------------------
# Health Check
# -----------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
