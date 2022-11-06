from datetime import datetime

from pydantic import BaseModel


class CommonBase(BaseModel):
    time_created: datetime | None = None
    time_updated: datetime | None = None
