from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
db_url = f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/{settings.POSTGRES_DB}'
async_engine = create_async_engine(
    db_url,
    echo=True,
)

async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# TODO: I don't feel like `declarative_base` belongs here.
Base = declarative_base()
