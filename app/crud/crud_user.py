from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_async_session, oauth2_scheme
from app.core.config import settings
from app.models.user import User
from app.schemas.token import TokenData
from app.schemas.user import UserInDB

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_user(user_id: int, session: AsyncSession):

    query = select(User).where(User.id == user_id)
    query_res = await session.execute(query)
    user = query_res.scalar()
    return UserInDB(**user.__dict__)


async def get_user_by_email(session: AsyncSession, email: str):
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    user = result.scalar()
    if not user:
        raise credentials_exception
    return UserInDB(**user.__dict__)


async def get_current_user(token: str = Depends(oauth2_scheme),  session: AsyncSession = Depends(get_async_session)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[
                             settings.ACCESS_TOKEN_ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = await get_user_by_email(email=token_data.email, session=session)
    if user is None:
        raise credentials_exception
    return user
