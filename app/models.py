from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field


class Todo(SQLModel, table=True):
    id: UUID = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    content: str = Field(index=True, min_length=3, max_length=54)
    is_completed: bool = Field(default=False)