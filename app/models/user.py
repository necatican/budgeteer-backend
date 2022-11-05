from uuid import uuid4

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4())
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # TODO: add salt
