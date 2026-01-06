from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.room import router as room_router
from app.routers.guest import router as guest_router
from app.routers.reservation import router as reservation_router
from app.routers.auth import router as auth_router


app = FastAPI(title="Hotel Management System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(reservation_router)
app.include_router(room_router)
app.include_router(guest_router)

@app.get("/")
def health_check():
    return {"status": "running"}
