from pydantic import BaseModel

# -----------------------------
# Order Schemas
# -----------------------------
class OrderCreate(BaseModel):
    name: str
    phone: str
    qty: int
    product_id: int

class OrderResponse(BaseModel):
    id: int
    name: str
    phone: str
    qty: int
    product_id: int
    payment_status: str

    class Config:
        from_attributes = True  # <-- changed from orm_mode

# -----------------------------
# Product Schemas
# -----------------------------
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    image_url: str | None = None

    class Config:
        from_attributes = True  # <-- changed from orm_mode

# -----------------------------
# Preorder Schemas
# -----------------------------
class PreorderCreate(BaseModel):
    customer_name: str
    customer_phone: str
    product_id: int

class PreorderResponse(BaseModel):
    id: int
    customer_name: str
    customer_phone: str
    product_id: int

    class Config:
        from_attributes = True
