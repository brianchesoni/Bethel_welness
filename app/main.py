from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import init_db, get_db
from app.routes import orders, products  # API routes
from app.models import Product

app = FastAPI(title="Bethel Wellness API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(orders.router, prefix="/api")
app.include_router(products.router, prefix="/api")  # Keep API routes under /api

# Serve frontend at /app (so it won't override API routes)
app.mount("/app", StaticFiles(directory="app/frontend_dist", html=True), name="frontend")

@app.on_event("startup")
def on_startup():
    init_db()

# Root route: return all products as JSON
@app.get("/")
def read_products(db: Session = Depends(get_db)):
    products_list = db.query(Product).all()
    return products_list

# Optional: API health check
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
