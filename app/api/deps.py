from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.crud_user import crud_user
from app.db.session import async_session
from app.schemas.token import TokenData

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/token")


async def get_async_session() -> Generator:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(token: str = Depends(oauth2_scheme),  session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
            settings.ACCESS_TOKEN_ALGORITHM])
        token_data = TokenData(**payload)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = await crud_user.get_by_email(email=token_data.sub, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
