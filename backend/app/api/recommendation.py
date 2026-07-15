from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.schemas.recommendation import RecommendationRequest
from app.services.recommendation_service import recommend_product

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

    best = recommend_product(
        db=db,
        budget=request.budget,
        category=request.category
    )

    if best is None:
        return {
            "message": "No products found."
        }

    return {
        "best_product": {
            "name": best.name,
            "brand": best.brand,
            "price": best.price,
            "rating": best.rating
        },
        "reason": f"{best.name} is recommended because it has a rating of {best.rating} and fits your budget."
    }