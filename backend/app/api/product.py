from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.product import Product
from app.schemas.product import ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# View all products
@router.get("/")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


# Add product
@router.post("/")
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        category=product.category,
        price=product.price,
        image=product.image
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {
        "message": "Product Added Successfully",
        "product": new_product
    }


# Search Products
@router.get("/search")
def search_products(
    name: str = Query(...),
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.name.ilike(f"%{name}%")
    ).all()

    return products


# Get Product by ID
@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"message": "Product not found"}

    return product

@router.get("/category/{category}")
def get_products_by_category(
    category: str,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.category.ilike(category)
    ).all()

    return products

@router.get("/price/{max_price}")
def get_products_by_price(
    max_price: float,
    db: Session = Depends(get_db)
):
    products = db.query(Product).filter(
        Product.price <= max_price
    ).all()

    return products 

@router.put("/{product_id}")
def update_product(
    product_id: int,
    updated_product: ProductCreate,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"message": "Product not found"}

    product.name = updated_product.name
    product.category = updated_product.category
    product.price = updated_product.price
    product.image = updated_product.image

    db.commit()
    db.refresh(product)

    return {
        "message": "Product updated successfully",
        "product": product
    }

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        return {"message": "Product not found"}

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully"
    }