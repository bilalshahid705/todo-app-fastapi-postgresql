from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from pydantic import BaseModel


class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    content: str = Field(index=True, min_length=3, max_length=54)
    is_completed: bool = Field(default=False)
    user_id: UUID = Field(foreign_key="user.id")


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, nullable=False)
    user_name: str
    email: str
    password: str

class Register_User (BaseModel):
    username: Annotated[str, Form()]
    email: Annotated[str, Form()]
    password: Annotated[str, Form()]