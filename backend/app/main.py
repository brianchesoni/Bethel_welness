from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os

from app.database import init_db, SessionLocal
from app.routes import orders, products
from app.models import Product

# -----------------------------
# FastAPI app
# -----------------------------
app = FastAPI(title="Bethel Wellness API")

# -----------------------------
# Enable CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Include API routers
# -----------------------------
app.include_router(orders.router, prefix="/api")    # /api/preorders
app.include_router(products.router, prefix="/api")  # /api/products

# -----------------------------
# Serve frontend build (Vite)
# -----------------------------
# Serve the frontend_dist folder (JS/CSS/images are directly in it)
app.mount("/frontend_dist", StaticFiles(directory="app/frontend_dist"), name="frontend_dist")

# Root route
@app.get("/")
def read_index():
    return FileResponse("app/frontend_dist/index.html")

# Catch-all route for SPA client-side routing
@app.get("/{full_path:path}")
def catch_all(full_path: str, request: Request):
    file_path = f"app/frontend_dist/{full_path}"
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse("app/frontend_dist/index.html")

# -----------------------------
# Populate default products
# -----------------------------
def populate_products():
    db: Session = SessionLocal()
    try:
        existing = db.query(Product).count()
        if existing == 0:
            default_products = [
                {"name": "Super Collagen Plus", "description": "Supports skin, hair, nails & joints", "price": 2500},
                {"name": "Vitamin C Complex", "description": "Boosts immunity and energy", "price": 1500},
                {"name": "Biotin Hair Boost", "description": "Healthy hair & nails", "price": 1800},
            ]
            for p in default_products:
                db.add(Product(**p))
            db.commit()
            print("✅ Default products populated!")
    except Exception as e:
        print("❌ Error populating products:", e)
    finally:
        db.close()

# -----------------------------
# Startup event
# -----------------------------
@app.on_event("startup")
def on_startup():
    print("Starting Bethel Wellness API...")
    init_db()
    populate_products()
    print("Startup complete.")

# -----------------------------
# Health check
# -----------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# -----------------------------
# Run app (for local/testing)
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))  # Dynamic port for Render
    uvicorn.run(app, host="0.0.0.0", port=port)
