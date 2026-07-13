from pydantic import BaseModel


class RecommendationRequest(BaseModel):
    budget: float
    category: str