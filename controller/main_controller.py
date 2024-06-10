from fastapi import APIRouter, HTTPException, Depends, status, Header
from sqlalchemy.orm import Session
from connection.connect import get_db
from service.user_service import UserService
from schemas.users import UserCreate, UserResponse
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

def verify_header(authorization: str = Header(...)):
    if authorization != os.getenv("AUTH_HEADER"):
        raise HTTPException(status_code=403, detail="Forbidden")

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_header)])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/country/{country}", response_model=List[UserResponse], dependencies=[Depends(verify_header)])
def get_users_by_country(country: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_users_by_country(country)

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(verify_header)])
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_header)])
def insert_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try: 
        user_service = UserService(db)
        created = user_service.insert_user(user_data.model_dump())
        if created:
            return {"message": "User inserted successfully"}
        else: 
            return {"message": "User already exists"}, status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
