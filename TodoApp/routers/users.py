from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import update
from ..models import Todos, Users
from starlette import status
from .auth import get_current_user, bcrypt_context

router = APIRouter(
    prefix="/Users",
    tags=["Users"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get("/Users", status_code=status.HTTP_200_OK)
async def get_users(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    if user_model is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_model

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependency, db: db_dependency,
                          user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password mismatch")
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

    # if user_model is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # db.query(Users).filter(Users.id == user.get("id")).update(
    #     {Users.hashed_password: bcrypt_context.hash(new_password) },
    #     synchronize_session="fetch"
    # )

@router.put("/{phone_number}", status_code=status.HTTP_204_NO_CONTENT)
async def update_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
