from uuid import UUID

from pydantic import BaseModel


class StatisticRowCreate(BaseModel):
    count: int
