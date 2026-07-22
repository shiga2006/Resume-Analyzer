from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from config import users_collection
import uuid
import datetime

auth_router = APIRouter(prefix="", tags=["Authentication"])


class UserSignup(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@auth_router.post("/signup")
def signup(user: UserSignup):
    if not user.username or not user.email or not user.password:
        raise HTTPException(status_code=400, detail="All fields are required")

    existing_user = users_collection.find_one({"email": user.email.lower()})
    if existing_user:
        return {"success": False, "message": "Email already registered"}

    user_doc = {
        "_id": str(uuid.uuid4()),
        "username": user.username,
        "email": user.email.lower(),
        "password": user.password,  # In production, use hashed passwords e.g. passlib
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    users_collection.insert_one(user_doc)
    return {
        "success": True,
        "message": "User registered successfully",
        "user": {
            "id": user_doc["_id"],
            "username": user_doc["username"],
            "email": user_doc["email"]
        }
    }


@auth_router.post("/login")
def login(credentials: UserLogin):
    user = users_collection.find_one({
        "email": credentials.email.lower(),
        "password": credentials.password
    })

    if not user:
        return {"success": False, "message": "Invalid email or password"}

    return {
        "success": True,
        "message": "Login successful",
        "user": {
            "id": str(user["_id"]),
            "username": user["username"],
            "email": user["email"]
        }
    }