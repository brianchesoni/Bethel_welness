from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import init_db, get_db, SessionLocal
from app.routes import orders, products
from app.models import Product

app = FastAPI(title="Bethel Wellness API")

# ---------------------------------------------------
# CORS SETTINGS
# ---------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# REGISTER API ROUTES
# ---------------------------------------------------
app.include_router(orders.router, prefix="/api")     # e.g. POST /api/preorders or /api/orders
app.include_router(products.router, prefix="/api")   # e.g. GET /api/products

# ---------------------------------------------------
# SERVE FRONTEND BUILD FROM Render
# ---------------------------------------------------
app.mount("/", StaticFiles(directory="app/frontend_dist", html=True), name="frontend")

# ---------------------------------------------------
# POPULATE DEFAULT PRODUCTS (SAFE VERSION)
# ---------------------------------------------------
def populate_products():
    """
    Adds default products if database is empty.
    Uses SessionLocal() instead of next(get_db()) which breaks on Render.
    """
    db: Session = SessionLocal()

    try:
        existing = db.query(Product).count()

        if existing == 0:
            default_products = [
                {
                    "name": "Super Collagen Plus",
                    "description": "Supports skin, hair, nails & joints",
                    "price": 2500,
                },
                {
                    "name": "Vitamin C Complex",
                    "description": "Boosts immunity and energy",
                    "price": 1500,
                },
                {
                    "name": "Biotin Hair Boost",
                    "description": "Healthy hair & nails",
                    "price": 1800,
                }
            ]

            for p in default_products:
                db.add(Product(**p))

            db.commit()
            print("Default products populated!")

    except Exception as e:
        print("❌ Error populating products:", e)

    finally:
        db.close()

# ---------------------------------------------------
# STARTUP EVENTS
# ---------------------------------------------------
@app.on_event("startup")
def on_startup():
    print("Starting Bethel Wellness API...")
    init_db()
    populate_products()
    print("Startup complete.")

# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
