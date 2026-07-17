from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from app.database import get_session, init_db
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate
from app.response import APIResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app: FastAPI = FastAPI(
    title="Todo App",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to dailyDo todo app",
        "data": None,
        "status": status.HTTP_200_OK,
    }


@app.post(
    "/todos/",
    response_model=APIResponse[Todo],
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    todo_data: TodoCreate,
    session: Annotated[Session, Depends(get_session)],
):
    todo = Todo(
        content=todo_data.content,
    ) 
    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {
        "message": "Todo created successfully",
        "data": todo,
        "status": status.HTTP_201_CREATED,
    }


@app.get(
    "/todos",
    response_model=APIResponse[list[Todo]],
    status_code=status.HTTP_200_OK,
)
async def get_all(
    session: Annotated[Session, Depends(get_session)],
):
    todo_list = session.exec(
        select(Todo)
    ).all()

    return {
        "message": "Todos fetched successfully",
        "data": todo_list,
        "status": status.HTTP_200_OK,
    }


@app.get(
    "/todos/{id}",
    response_model=APIResponse[Todo],
    status_code=status.HTTP_200_OK,
)
async def get_single_todo(
    id: str,
    session: Annotated[Session, Depends(get_session)],
):
    todo = session.exec(
        select(Todo).where(Todo.id == id)
    ).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    return {
        "message": "Todo fetched successfully",
        "data": todo,
        "status": status.HTTP_200_OK,
    }


@app.put(
    "/todos/{id}",
    response_model=APIResponse[Todo],
    status_code=status.HTTP_200_OK,
)
async def edit_todo(
    id: str,
    todo: TodoUpdate,
    session: Annotated[Session, Depends(get_session)],
):
    updated_todo = session.exec(
        select(Todo).where(Todo.id == id)
    ).first()

    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    updated_todo.content = todo.content
    updated_todo.is_completed = todo.is_completed

    session.add(updated_todo)
    session.commit()
    session.refresh(updated_todo)

    return {
        "message": "Todo updated successfully",
        "data": updated_todo,
        "status": status.HTTP_200_OK,
    }


@app.delete(
    "/todos/{id}",
    response_model=APIResponse[None],
    status_code=status.HTTP_200_OK,
)
async def delete_todo(
    id: str,
    session: Annotated[Session, Depends(get_session)],
):
    deleted_todo = session.exec(
        select(Todo).where(Todo.id == id)
    ).first()

    if not deleted_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    session.delete(deleted_todo)
    session.commit()

    return {
        "message": "Todo deleted successfully",
        "data": None,
        "status": status.HTTP_200_OK,
    }