from fastapi import APIRouter, HTTPException, Depends
from app.schemas.reservation import (
    ReservationCreate,
    ReservationResponse,
    WalkInReservation,
    ReservationDetailResponse
)
from app.services.reservation import (
    create_reservation_service,
    check_in_service,
    check_out_service,
    get_active_reservations_service,
    walk_in_reservation_service,
    get_reservations_by_room_service
)
from app.repositories.guest import get_guest_by_id
from app.repositories.room import get_room_by_id
from app.core.security import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"], dependencies=[Depends(get_current_user)])

@router.post("/", response_model=ReservationResponse)
def create_reservation(
    reservation: ReservationCreate,
):
    try:
        new_res = create_reservation_service(reservation.dict())
        
        # Fetch guest and room details for response
        guest = get_guest_by_id(new_res["guest_id"])
        room = get_room_by_id(new_res["room_id"])
        
        # Convert datetime back to date for response
        check_in = new_res["check_in_date"]
        check_out = new_res["check_out_date"]
        
        if hasattr(check_in, 'date'):
            check_in = check_in.date()
        if hasattr(check_out, 'date'):
            check_out = check_out.date()
        
        return {
            "id": str(new_res["_id"]),
            "guest_name": guest["name"],
            "room_number": room["room_number"],
            "phone_number": guest["phone"],
            "check_in_date": check_in,
            "check_out_date": check_out,
            "status": new_res["status"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/all", response_model=list[ReservationResponse])
def get_all_reservations():
    reservations = get_active_reservations_service()
    response = []
    for res in reservations:
        guest = get_guest_by_id(res["guest_id"])
        room = get_room_by_id(res["room_id"])
        
        # Convert datetime back to date for response
        check_in = res["check_in_date"]
        check_out = res["check_out_date"]
        
        if hasattr(check_in, 'date'):
            check_in = check_in.date()
        if hasattr(check_out, 'date'):
            check_out = check_out.date()
        
        response.append({
            "id": str(res["_id"]),
            "guest_name": guest["name"],
            "room_number": room["room_number"],
            "phone_number": guest["phone"],
            "check_in_date": check_in,
            "check_out_date": check_out,
            "status": res["status"]
        })
    return response
@router.post("/{reservation_id}/check-in")
def check_in(
    reservation_id: str,
):
    try:
        check_in_service(reservation_id)
        return {"message": "Checked in successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{reservation_id}/check-out")
def check_out(
    reservation_id: str,
):
    try:
        check_out_service(reservation_id)
        return {"message": "Checked out successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/walk-in", response_model=ReservationResponse)
def walk_in_reservation(reservation: WalkInReservation):
    """
    Handle walk-in reservations with custom pricing.
    Supports both existing guests (using guest_id) and new guests (using name, phone, id_proof).
    """
    try:
        new_res = walk_in_reservation_service(reservation.model_dump())
        
        # Fetch guest and room details for response
        guest = get_guest_by_id(new_res["guest_id"])
        room = get_room_by_id(new_res["room_id"])
        
        # Convert datetime back to date for response
        check_in = new_res["check_in_date"]
        check_out = new_res["check_out_date"]
        
        if hasattr(check_in, 'date'):
            check_in = check_in.date()
        if hasattr(check_out, 'date'):
            check_out = check_out.date()
        
        return {
            "id": str(new_res["_id"]),
            "guest_name": guest["name"],
            "room_number": room["room_number"],
            "phone_number": guest["phone"],
            "check_in_date": check_in,
            "check_out_date": check_out,
            "status": new_res["status"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/room/{room_id}", response_model=list[ReservationDetailResponse])
def get_reservations_by_room(room_id: str):
    """Fetch all reservations for a specific room with complete details"""
    try:
        reservations = get_reservations_by_room_service(room_id)
        room = get_room_by_id(room_id)
        
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        response = []
        for res in reservations:
            # Convert datetime back to date for response
            check_in = res["check_in_date"]
            check_out = res["check_out_date"]
            
            if hasattr(check_in, 'date'):
                check_in = check_in.date()
            if hasattr(check_out, 'date'):
                check_out = check_out.date()
            
            response.append({
                "id": str(res["_id"]),
                "guest_id": res["guest_id"],
                "guest_name": res.get("guest_name", ""),
                "guest_phone": res.get("guest_phone", ""),
                "guest_email": res.get("guest_email", ""),
                "guest_id_proof": res.get("guest_id_proof", ""),
                "room_id": res["room_id"],
                "room_number": room["room_number"],
                "check_in_date": check_in,
                "check_out_date": check_out,
                "total_amount": res.get("total_amount"),
                "price_per_night": res.get("price_per_night"),
                "status": res["status"]
            })
        
        return response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/room/{room_id}/current", response_model=ReservationDetailResponse)
def get_current_guest_by_room(room_id: str):
    """Fetch only the currently checked-in guest for a specific room"""
    try:
        reservations = get_reservations_by_room_service(room_id)
        room = get_room_by_id(room_id)
        
        if not room:
            raise HTTPException(status_code=404, detail="Room not found")
        
        # Find the checked-in reservation
        current_reservation = next(
            (res for res in reservations if res["status"] == "CHECKED_IN"), 
            None
        )
        
        if not current_reservation:
            raise HTTPException(status_code=404, detail="No guest currently checked in")
        
        res = current_reservation
        check_in = res["check_in_date"]
        check_out = res["check_out_date"]
        
        if hasattr(check_in, 'date'):
            check_in = check_in.date()
        if hasattr(check_out, 'date'):
            check_out = check_out.date()
        
        return {
            "id": str(res["_id"]),
            "guest_id": res["guest_id"],
            "guest_name": res.get("guest_name", ""),
            "guest_phone": res.get("guest_phone", ""),
            "guest_email": res.get("guest_email", ""),
            "guest_id_proof": res.get("guest_id_proof", ""),
            "room_id": res["room_id"],
            "room_number": room["room_number"],
            "check_in_date": check_in,
            "check_out_date": check_out,
            "total_amount": res.get("total_amount"),
            "price_per_night": res.get("price_per_night"),
            "status": res["status"]
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
