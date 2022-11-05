from datetime import datetime

from pydantic import BaseModel


class CommonBase(BaseModel):
    time_created: datetime
    time_updated: datetime | None = None
