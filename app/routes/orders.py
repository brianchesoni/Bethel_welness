from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Preorder

router = APIRouter(prefix="/preorders", tags=["Preorders"])

# Request body for creating a preorder
class PreorderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    product_id: int

@router.post("/", tags=["Preorders"])
def create_preorder(order: PreorderRequest, db: Session = Depends(get_db)):
    """
    Create a new preorder
    """
    preorder = Preorder(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        product_id=order.product_id
    )
    db.add(preorder)
    db.commit()
    db.refresh(preorder)

    return {"message": "Preorder saved!", "order_id": preorder.id}
