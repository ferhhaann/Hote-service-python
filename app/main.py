from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.room import router as room_router
from app.routers.guest import router as guest_router
from app.routers.reservation import router as reservation_router
from app.routers.auth import router as auth_router
from app.core.config import get_settings
from app.core.database import db

settings = get_settings()

app = FastAPI(title="Hotel Management System")

# CORS configuration from environment
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(reservation_router)
app.include_router(room_router)
app.include_router(guest_router)

@app.get("/")
def root():
    return {"message": "Hotel Management API", "version": "1.0.0"}

@app.get("/health")
def health_check():
    try:
        # Ping database to verify connection
        db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
