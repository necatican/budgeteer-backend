from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
