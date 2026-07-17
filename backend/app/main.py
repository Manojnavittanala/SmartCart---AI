from app.api import recommendation
from app.api import product
from fastapi import FastAPI

from app.services.gemini_service import ask_gemini
from app.api import auth
from app.database.database import Base, engine
from app.models.user import User
from app.models.product import Product

app = FastAPI(
    title="SmartCart AI",
    description="AI Multi-Agent Shopping Assistant",
    version="1.0.0"
)
Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(product.router)
app.include_router(recommendation.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to SmartCart AI 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "Running",
        "project": "SmartCart AI"
    }

@app.get("/test-gemini")
def test_gemini():
    response = ask_gemini("Say hello in one sentence.")
    return {"response": response}