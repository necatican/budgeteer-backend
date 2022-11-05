from sqlalchemy import Column, String

from app.db.session import Base
from app.models.common import CommonUUID


class User(CommonUUID, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # TODO: add salt
