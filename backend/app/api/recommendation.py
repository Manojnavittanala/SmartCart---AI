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
    .order_by(Product.price.desc())
    .all()
)