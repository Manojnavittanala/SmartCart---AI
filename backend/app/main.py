from fastapi import FastAPI
from app.api import auth

app = FastAPI(
    title="SmartCart AI",
    description="AI Multi-Agent Shopping Assistant",
    version="1.0.0"
)

app.include_router(auth.router)


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