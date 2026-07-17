from sqlmodel import SQLModel, create_engine, Session
from . import settings

database_url = str(settings.DATABASE_URL).replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(database_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)

# Aik possibility ya ha ka hum session close karna bhool jaye. 
# Iss liya with loop use karty han. Means jab session complete ho tou session close ho jaye khud he.
def get_session():
    with Session(engine) as session: 
        yield session

# yield is a keyword used to pause a function temporarily and return a value to the caller, 
# while keeping the function's internal state intact so it can resume exactly where it left off later.