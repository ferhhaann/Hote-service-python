from app.repositories.user import create_user, get_user_by_email
from app.core.security import hash_password, verify_password, create_access_token

def register_user_service(email: str, password: str, role: str):
    if get_user_by_email(email):
        raise Exception("User already exists")

    user_data = {
        "email": email,
        "hashed_password": hash_password(password),
        "role": role,
        "is_active": True
    }

    create_user(user_data)
    return user_data

def authenticate_user_service(email: str, password: str):
    user = get_user_by_email(email)
    if not user:
        return None

    if not verify_password(password, user["hashed_password"]):
        return None

    token = create_access_token({
        "sub": str(user["_id"]),
        "email": user["email"],
        "role": user["role"]
    })

    return token
