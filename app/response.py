from typing import Generic, TypeVar
from pydantic import BaseModel


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    message: str
    data: T | None = None
    status: int