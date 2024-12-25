from uuid import UUID

from pydantic import BaseModel


class PartnerAggregateCreate(BaseModel):
    user_id: UUID
    name: str
    address: str
    email: str
    phone: str
