from app.database import SessionLocal, init_db
from app.models import Product

# Initialize tables
init_db()

db = SessionLocal()

# Sample products
sample_products = [
    {"name": "Herbal Tea", "description": "Relaxing tea blend", "price": 10, "image_url": None},
    {"name": "Vitamin Gummies", "description": "Vitamin C & D", "price": 15, "image_url": None},
    {"name": "Essential Oil", "description": "Lavender scented", "price": 20, "image_url": None},
]

# Insert products
for prod in sample_products:
    product = Product(**prod)
    db.add(product)

db.commit()
db.close()

print("Sample products added!")
