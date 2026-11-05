import os
import jwt

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from pwdlib import PasswordHash

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.connection import SessionLocal
from database.models import User


# ==========================================
# CONFIGURATION
# ==========================================

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM", "HS256")

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
)

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY missing from .env")


# ==========================================
# PASSWORD HASHING
# ==========================================

password_hash = PasswordHash.recommended()


def hash_password(password: str):

    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str):

    return password_hash.verify(
        password,
        hashed_password
    )


# ==========================================
# JWT TOKEN GENERATION
# ==========================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# ==========================================
# DATABASE SESSION
# ==========================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ==========================================
# AUTHENTICATED USER
# ==========================================

def get_current_user(

    token: str = Depends(oauth2_scheme),

    db: Session = Depends(get_db)

):

    credentials_exception = HTTPException(

        status_code=status.HTTP_401_UNAUTHORIZED,

        detail="Invalid or expired authentication token",

        headers={
            "WWW-Authenticate": "Bearer"
        }

    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (jwt.InvalidTokenError, TypeError, ValueError):

        raise credentials_exception

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if user is None:
        raise credentials_exception

    return user