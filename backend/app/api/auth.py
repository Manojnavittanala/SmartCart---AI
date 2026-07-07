from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister, UserLogin
from app.core.security import hash_password

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

# Temporary in-memory database
users = []


@router.post("/register")
def register(user: UserRegister):

    # Check duplicate email
    for existing_user in users:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

    hashed_password = hash_password(user.password)

    new_user = {
        "full_name": user.full_name,
        "email": user.email,
        "password": hashed_password
    }

    users.append(new_user)

    return {
        "message": "Registration successful"
    }


@router.post("/login")
def login(user: UserLogin):

    return {
        "message": "Login API - Coming Soon"
    }