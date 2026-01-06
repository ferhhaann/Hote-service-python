from app.core.database import db

user_collection = db["users"]

def create_user(user_data: dict):
    user_collection.insert_one(user_data)
    return user_data

def get_user_by_email(email: str):
    return user_collection.find_one({"email": email})
