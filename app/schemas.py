from sqlmodel import SQLModel, Field


class TodoCreate(SQLModel):
    content: str = Field(
        min_length=3,
        max_length=54,
    )

class TodoUpdate(SQLModel):
    content: str = Field(
        min_length=3,
        max_length=54,
    )
    is_completed: bool