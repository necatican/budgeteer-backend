from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# TODO: Check other algorithms and use salt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(
        data: dict,
        expires_delta: timedelta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
):
    to_encode = data.copy()

    expire = datetime.utcnow() + expires_delta

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ACCESS_TOKEN_ALGORITHM
    )

    return encoded_jwt
