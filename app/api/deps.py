
from typing import Generator

from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.db.session import async_session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/token")


async def get_async_session() -> Generator:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
