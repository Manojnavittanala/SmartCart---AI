from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import re

from app.schemas.ai import AIRequest, CompareRequest
from app.services.gemini_service import ask_gemini
from app.models.product import Product
from app.database.database import SessionLocal

router = APIRouter(prefix="/ai", tags=["AI"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/recommend")
def recommend(request: AIRequest, db: Session = Depends(get_db)):

    query = request.query.lower()

    products_query = db.query(Product)

    if "laptop" in query:
        products_query = products_query.filter(
            Product.category.ilike("%laptop%")
        )

    elif "phone" in query or "mobile" in query:
        products_query = products_query.filter(
            Product.category.ilike("%phone%")
        )

    elif "headphone" in query:
        products_query = products_query.filter(
            Product.category.ilike("%headphone%")
        )

    products = products_query.all()

    budget = re.search(r"(\d+)", request.query.replace(",", ""))

    if budget:
        max_price = float(budget.group(1))
        products = [p for p in products if p.price <= max_price]

    if not products:
        return {
            "response": "Sorry, I couldn't find any matching products."
        }

    product_list = ""

    for p in products:
        product_list += f"""
Name: {p.name}
Brand: {p.brand}
Category: {p.category}
Price: ₹{p.price}
Rating: {p.rating}
Description: {p.description}

"""

    prompt = f"""
You are SmartCart AI.

Available Products:

{product_list}

Customer Question:
{request.query}

Recommend ONLY from the available products.

Explain:

1. Best option
2. Why
3. Pros
4. Value for money
"""

    answer = ask_gemini(prompt)

    return {"response": answer}


@router.post("/compare")
def compare_products(request: CompareRequest,
                     db: Session = Depends(get_db)):

    p1 = db.query(Product).filter(
        Product.name.ilike(f"%{request.product1}%")
    ).first()

    p2 = db.query(Product).filter(
        Product.name.ilike(f"%{request.product2}%")
    ).first()

    if not p1 or not p2:
        return {
            "response": "One or both products were not found."
        }

    prompt = f"""
Compare these two SmartCart products.

Product 1

Name: {p1.name}

Brand: {p1.brand}

Category: {p1.category}

Price: ₹{p1.price}

Rating: {p1.rating}

Description: {p1.description}


Product 2

Name: {p2.name}

Brand: {p2.brand}

Category: {p2.category}

Price: ₹{p2.price}

Rating: {p2.rating}

Description: {p2.description}

Compare them based on:

• Performance

• Price

• Rating

• Value for money

Finally tell which product you recommend and why.
"""

    answer = ask_gemini(prompt)

    return {"response": answer}