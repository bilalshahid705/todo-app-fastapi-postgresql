from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.database import get_db
from fastapi import Depends
from sqlmodel import Session, select
from typing import Annotated
from app.models import User

password_hash = PasswordHash((BcryptHasher(),))

def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def get_user_from_db(
    db: Session,
    user_name: str | None = None,
    email: str | None = None,
):
    user = db.exec(
        select(User).where(User.user_name == user_name)
    ).first()

    if user:
        return user

    return db.exec(
        select(User).where(User.email == email)
    ).first()