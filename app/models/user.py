from sqlalchemy import Column, String

from app.db.session import Base
from app.models.common import CommonUUID


class User(CommonUUID, Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    # accounts = relationship("Account", back_populates="owner", lazy="noload")
    # TODO: add salt
    # TODO: add permissions (for shared profiles, read-only groups)
