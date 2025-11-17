from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.database import init_db
from app.routes import orders, products  # <- include products

app = FastAPI(title="Bethel Wellness API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(orders.router)
app.include_router(products.router)  # <- keep API routes

# Serve frontend
# Make sure you have copied your Vite 'dist' folder here:
# backend/app/frontend_dist
app.mount("/", StaticFiles(directory="app/frontend_dist", html=True), name="frontend")

@app.on_event("startup")
def on_startup():
    init_db()

# Optional: API health check (this will be at /api or any other path you want)
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
