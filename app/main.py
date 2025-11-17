from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
app.include_router(products.router)  # <- add this

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def home():
    return {"message": "Bethel Wellness API is running!"}
