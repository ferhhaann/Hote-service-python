from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserLogin
from app.services.user import (
    register_user_service,
    authenticate_user_service
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(payload: UserCreate):
    try:
        user = register_user_service(
            payload.email,
            payload.password,
            payload.role
        )
        return {
            "email": user["email"],
            "role": user["role"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(payload: UserLogin):
    token = authenticate_user_service(payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "access_token": token,
        "token_type": "bearer"
    }
