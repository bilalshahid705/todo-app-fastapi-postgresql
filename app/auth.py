from passlib.context import CryptContext
from app.core.database import get_db
from fastapi import Depends
from sqlmodel import Session, select
from typing import Annotated
from app.models import User

pwd_context = CryptContext(schemes="bcrypt")

def hash_password(password):
    return pwd_context.hash(password)


def get_user_from_db(db: Annotated[Session, Depends(get_db)], user_name: str, emai: str):
    
    statement = select(User).where(User.user_name == user_name)
    user = db.exec(statement).first()
    if not user:
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()
        if user: 
            return user
    return user