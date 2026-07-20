from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.ai import AIRequest
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

    products = db.query(Product).all()

    product_list = ""

    for p in products:
        product_list += (
            f"Name: {p.name}, "
            f"Brand: {p.brand}, "
            f"Category: {p.category}, "
            f"Price: ₹{p.price}, "
            f"Rating: {p.rating}\n"
        )

    prompt = f"""
You are an AI shopping assistant.

These are the products available in SmartCart:

{product_list}

Customer Question:
{request.query}

Recommend only from the products listed above.
Explain why they are good choices.
"""

    response = ask_gemini(prompt)

    return {"response": response}