from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, status

from app.api import api_router
from app.core.database import init_db
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app: FastAPI = FastAPI(
    title="Todo App",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://localhost:8000", "https://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)



app.include_router(api_router, prefix="/api/v1")