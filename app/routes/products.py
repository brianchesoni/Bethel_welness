from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product

router = APIRouter(tags=["Products"])

# GET /api/products
@router.get("/products", tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    """Fetch all products"""
    return db.query(Product).all()
