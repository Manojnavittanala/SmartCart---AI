from fastapi import APIRouter
from app.schemas.user import UserRegister, UserLogin

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(user: UserRegister):
    return {
        "message": "User registered successfully",
        "user": user
    }


@router.post("/login")
def login(user: UserLogin):
    return {
        "message": "Login successful",
        "email": user.email
    }