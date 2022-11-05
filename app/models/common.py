from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql.functions import now
from sqlalchemy.types import DateTime


class CommonBase(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    time_created = Column(DateTime, server_default=now(), nullable=False)
    time_updated = Column(DateTime, onupdate=now())


class CommonUUID(CommonBase):
    id = Column(UUID(as_uuid=True), primary_key=True,
                index=True, default=uuid4())
