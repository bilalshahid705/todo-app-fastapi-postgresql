from fastapi import APIRouter

api_router = APIRouter()

from app.api.v1.user import router as user_router
from app.api.v1.todo import router as todo_router

@api_router.get("/")
async def home():
    return {"message": "Welcome to the API"}


@api_router.get("/health")
async def health_check():
    return {"status": "API is working fine!"}


api_router.include_router(user_router)
api_router.include_router(todo_router)