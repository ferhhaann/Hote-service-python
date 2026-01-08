from pymongo import MongoClient
from app.core.config import get_settings

settings = get_settings()

client = MongoClient(
    settings.MONGODB_URL,
    maxPoolSize=50,
    minPoolSize=10,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000
)
db = client[settings.DATABASE_NAME]

room_collection = db["rooms"]
