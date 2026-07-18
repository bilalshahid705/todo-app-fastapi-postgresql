from sqlmodel import SQLModel, create_engine, Session
from . import settings

database_url = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session: 
        yield session