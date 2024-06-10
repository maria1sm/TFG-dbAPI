from fastapi import APIRouter, HTTPException, Depends, status, Header
from fastapi.openapi.models import APIKeyIn, APIKeyIn, SecurityScheme
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from connection.connect import get_db
from service.user_service import UserService
from schemas.users import UserCreate, UserResponse
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

api_key_header = APIKeyHeader(name="authorization", auto_error=False)

def verify_header(authorization: str = Header(...)):
    if authorization != os.getenv("AUTH_HEADER"):
        raise HTTPException(status_code=403, detail="Forbidden")

# This dependency is for Swagger UI documentation
def get_api_key(api_key_header: str = Header(...)):
    return api_key_header

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(verify_header)], tags=["users"])
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/country/{country}", response_model=List[UserResponse], dependencies=[Depends(verify_header)], tags=["users"])
def get_users_by_country(country: str, db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_users_by_country(country)

@router.get("/", response_model=List[UserResponse], dependencies=[Depends(verify_header)], tags=["users"])
def get_all_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    return user_service.get_all_users()

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_header)], tags=["users"])
def insert_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        created = user_service.insert_user(user_data.dict())
        if created:
            return {"message": "User inserted successfully"}
        else:
            return {"message": "User already exists"}, status.HTTP_200_OK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Include the API Key in the OpenAPI schema
api_key_scheme = SecurityScheme(
    type="apiKey",
    name="Authorization",
    in_=APIKeyIn.header
)

# Update the router OpenAPI schema
router.openapi_schema = {
    "components": {
        "securitySchemes": {
            "api_key_header": api_key_scheme
        }
    },
    "security": [
        {"api_key_header": []}
    ]
}
