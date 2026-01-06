from app.core.database import db
from bson import ObjectId

guest_collection = db["guests"]

def create_guest(guest_data: dict):
    result = guest_collection.insert_one(guest_data)
    guest_data["_id"] = result.inserted_id
    return guest_data

def get_guests():
    guests = []
    for guest in guest_collection.find():
        guest["_id"] = str(guest["_id"])
        guests.append(guest)
    return guests

def get_guest_by_id(guest_id: str):
    guest = guest_collection.find_one({"_id": ObjectId(guest_id)})
    if guest:
        guest["_id"] = str(guest["_id"])
    return guest

def get_guest_by_phone(phone: str):
    guest = guest_collection.find_one({"phone": phone})
    if guest:
        guest["_id"] = str(guest["_id"])
    return guest

def get_guest_by_id_proof(id_proof: str):
    guest = guest_collection.find_one({"id_proof": id_proof})
    if guest:
        guest["_id"] = str(guest["_id"])
    return guest
