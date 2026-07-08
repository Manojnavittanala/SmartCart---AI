from app.api import product
from fastapi import FastAPI

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