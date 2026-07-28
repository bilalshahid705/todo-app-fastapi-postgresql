from pwdlib import PasswordHash
from pwdlib.hashers.bcrypt import BcryptHasher
from app.core.database import get_db
from fastapi import Depends
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from app.models import User
from datetime import datetime, timezone, timedelta

EXPIRY_TIME = 1

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/token")

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

def authenticate_user(username, password, db: Annotated[Session, Depends(get_db)]):
    db_user = get_user_from_db(db=db, username=username)
    print(f""" authenticate {db_user} """)
    if not db_user:
        return False
    if not verify_password(password, db_user.password):
        return False
    return db_user


def create_access_token(data: dict, expiry_time: timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, SECRET_KEY, algorithm=ALGORITHYM, )
    return encoded_jwt


def current_user(token: Annotated[str, Depends(oauth_scheme)], db: Annotated[Session, Depends(get_db)]):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        username: str | None = payload.get("sub")

        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credential_exception
    user = get_user_from_db(db, username=token_data.username)
    if not user:
        raise credential_exception
    return user


def create_refresh_token(data: dict, expiry_time: timedelta | None):
    data_to_encode = data.copy()
    if expiry_time:
        expire = datetime.now(timezone.utc) + expiry_time
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data_to_encode, SECRET_KEY, algorithm=ALGORITHYM, )
    return encoded_jwt


def validate_refresh_token(token: str, db: Annotated[Session, Depends(get_db)]):

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token, Please login again",
        headers={"www-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHYM)
        email: str | None = payload.get("sub")
        if email is None:
            raise credential_exception
        token_data = RefreshTokenData(email=email)

    except:
        raise JWTError
    user = get_user_from_db(db, email=token_data.email)
    if not user:
        raise credential_exception
    return user