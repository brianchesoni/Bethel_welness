from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routes import preorders, products  # <-- use preorders.py instead of orders.py

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
app.include_router(preorders.router, prefix="/api")  # POST /api/preorders
app.include_router(products.router, prefix="/api")   # GET /api/products

# -----------------------------
# Serve frontend at root /
# -----------------------------
app.mount("/", StaticFiles(directory="app/frontend_dist", html=True), name="frontend")

# -----------------------------
# Startup event: initialize DB
# -----------------------------
@app.on_event("startup")
def on_startup():
    init_db()

# -----------------------------
# Optional: API health check
# -----------------------------
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
