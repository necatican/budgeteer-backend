
from typing import Any, Dict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import models
from app.core.auth import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.schemas.user import UserCreate, UserInDB, UserUpdate


class CRUDUser(CRUDBase[models.User, UserCreate, UserUpdate]):
    async def get_by_email(self, session: AsyncSession, email: str):
        query = select(models.User).where(models.User.email == email)
        result = await session.execute(query)
        res = result.scalar()
        if not res:
            return None
        return res

    async def authenticate_user(self, email: str, password: str, session: AsyncSession):
        user = await crud_user.get_by_email(session, email=email)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

    async def create(self, session: AsyncSession, obj_in: UserCreate):
        db_obj = models.User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password)
        )

        res = await super().create(session, obj_in=db_obj)

        return res

    async def update(
        self,
        session: AsyncSession,
        patch: UserUpdate | Dict[str, Any],
        current_user: models.User,
    ):

        # password/hashed_password is an exception since the field name changes during an update
        if patch.password is not None:
            hashed_password = hashed_password = get_password_hash(
                patch.password)
        else:
            hashed_password = current_user.hashed_password

        res = await super().update(
            session,
            db_obj=current_user,
            obj_in=UserInDB(
                hashed_password=hashed_password,
            )
        )

        return res


crud_user = CRUDUser(models.User)
