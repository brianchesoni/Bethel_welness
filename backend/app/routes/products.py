# backend/app/routes/products.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product

# /api/products
router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/", response_model=list[dict])
def get_products(db: Session = Depends(get_db)):
    """
    Fetch all products from the database.
    """
    products = db.query(Product).all()

    if not products:
        return []   # No products yet

    # Convert SQLAlchemy objects to clean JSON dictionaries
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "image_url": p.image_url
        }
        for p in products
    ]
