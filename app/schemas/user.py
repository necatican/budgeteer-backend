from uuid import UUID

from app.schemas.common import CommonBase


class UserBase(CommonBase):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: UUID

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
