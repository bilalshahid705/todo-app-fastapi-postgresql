from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from app.models import RegisterUser, User
from app.auth import get_user_from_db, hash_password
from sqlmodel import Session, select
from app.core.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_user():
    return {"message": "Welcome to the Todo User Page"}


@router.post("/register")
async def register_user(new_user: Annotated[RegisterUser, Depends()],
                        db: Annotated[Session, Depends(get_db)]):
    db_user = get_user_from_db(db, new_user.user_name, new_user.email)

    if db_user:
        raise HTTPException(
            status_code=409,
            detail="User with these credentials already exists."
        )
    
    user = User(user_name = new_user.user_name,
                email = new_user.email,
                password = hash_password(new_user.password))

    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": f""" User with {user.user_name} successfully registered """}

# @router.get('/me')
# async def user_profile (current_user:Annotated[User, Depends(current_user)]):

#     return current_user