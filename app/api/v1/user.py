from fastapi import APIRouter, Depends
from typing import Annotated
from app.models import Register_User

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}}
)

@router.get("/")
async def read_user():
    return {"message": "Welcome to the Todo User Page"}

@router.post("/register")
async def register_user(new_user: Annotated[Register_User, Depends()]):
    pass