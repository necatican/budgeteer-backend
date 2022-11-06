from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        q = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return q.scalar()

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:

        # For info on scalars(): https://docs.sqlalchemy.org/en/14/orm/session_basics.html#querying-2-0-style
        q = await session.execute(select(self.model).order_by(self.model.id).limit(limit).offset(skip))

        return q.scalars().all()

    async def create(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        session.add(obj_in)

        await session.commit()
        await session.refresh(obj_in)

        return obj_in

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in:  UpdateSchemaType | Dict[str, Any]
    ) -> ModelType:

        obj_data = db_obj.__dict__
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, session: AsyncSession, *, id: UUID | str | int) -> ModelType:
        obj = await self.get(session, id=id)

        await session.delete(obj)
        await session.commit()
        return obj
