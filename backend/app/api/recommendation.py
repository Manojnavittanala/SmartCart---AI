from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.models.product import Product
from app.schemas.recommendation import RecommendationRequest

router = APIRouter(
    prefix="/recommend",
    tags=["AI Recommendation"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def recommend(
    request: RecommendationRequest,
    db: Session = Depends(get_db)
):

    products = (
        db.query(Product)
        .filter(
            Product.category.ilike(request.category),
            Product.price <= request.budget
        )
        .order_by(Product.rating.desc())
        .all()
    )

    if not products:
        return {
            "message": "No products found within your budget."
        }

    best = products[0]

    return {
        "best_product": {
            "name": best.name,
            "brand": best.brand,
            "price": best.price,
            "rating": best.rating
        },
        "reason": (
            f"{best.name} is recommended because it has a rating of "
            f"{best.rating}, fits your budget, and belongs to the "
            f"{best.category} category."
        )
    }