from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Preorder

router = APIRouter(prefix="/orders", tags=["Orders"])

class PreorderRequest(BaseModel):
    customer_name: str
    customer_phone: str
    product_id: int

@router.post("/", tags=["Orders"])
def create_preorder(order: PreorderRequest, db: Session = Depends(get_db)):
    preorder = Preorder(
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        product_id=order.product_id
    )
    db.add(preorder)
    db.commit()
    db.refresh(preorder)

    return {"message": "Preorder saved!", "order_id": preorder.id}
