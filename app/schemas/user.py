from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.schemas.common import CommonBase


# TODO: Decide the CommonBase structure.
# time_created/time_updated should be only available for the backend
class UserBase(CommonBase):
    email: EmailStr | None = None


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    password: str | None = None


class UserInDBBase(UserBase):
    id: UUID | None = None

    class Config:
        orm_mode = True

# Additional properties to return via API


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
