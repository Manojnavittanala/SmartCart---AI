from fastapi import APIRouter, HTTPException
from app.schemas.user import UserRegister, UserLogin
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.schemas.token import Token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

from app.schemas.token import Token

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


@router.post("/login", response_model=Token)
def login(user: UserLogin):

    for existing_user in users:

        if existing_user["email"] == user.email:

            if verify_password(
                user.password,
                existing_user["password"]
            ):

                access_token = create_access_token(
                    data={
                        "sub": existing_user["email"]
                    }
                )

                return {
                    "access_token": access_token,
                    "token_type": "bearer"
                }

            raise HTTPException(
                status_code=401,
                detail="Invalid password"
            )

    raise HTTPException(
        status_code=404,
        detail="User not found"
    )