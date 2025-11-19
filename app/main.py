from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import init_db, get_db
from app.routes import orders, products  # API routers
from app.models import Product

app = FastAPI(title="Bethel Wellness API")

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include API routers under /api
# -----------------------------
app.include_router(orders.router, prefix="/api")   # POST /api/orders
app.include_router(products.router, prefix="/api") # GET /api/products

# -----------------------------
# Serve frontend at root /
# -----------------------------
app.mount("/", StaticFiles(directory="app/frontend_dist", html=True), name="frontend")

# -----------------------------
# Startup event: initialize DB & populate products
# -----------------------------
@app.on_event("startup")
def on_startup():
    init_db()
    populate_products()

def populate_products():
    """
    Insert default products if the table is empty.
    """
    db = next(get_db())
    existing = db.query(Product).count()
    if existing == 0:
        default_products = [
            {
                "name": "Super Collagen Plus",
                "description": "Supports skin, hair, nails & joints",
                "price": 2500
            },
            {
                "name": "Vitamin C Complex",
                "description": "Boosts immunity and energy",
                "price": 1500
            },
            {
                "name": "Biotin Hair Boost",
                "description": "Healthy hair & nails",
                "price": 1800
            }
        ]
        for p in default_products:
            product = Product(**p)
            db.add(product)
        db.commit()
        print("Default products populated!")

# -----------------------------
# Optional: API health check
# -----------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
