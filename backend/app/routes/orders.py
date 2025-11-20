# backend/app/routes/orders.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Preorder, Product

router = APIRouter(prefix="/orders", tags=["Orders"])

# -----------------------------
# Request Body Schema
# -----------------------------
class PreorderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    product_id: int

# -----------------------------
# Create a Preorder
# POST /api/orders
# -----------------------------
@router.post("/")
def create_preorder(order: PreorderRequest, db: Session = Depends(get_db)):

    # Check product exists
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Create preorder
    preorder = Preorder(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        product_id=order.product_id
    )

    db.add(preorder)
    db.commit()
    db.refresh(preorder)

    return {"message": "Preorder saved!", "order_id": preorder.id}
