from uuid import UUID
from datetime import datetime
from decimal import Decimal

from typing import Optional

from pydantic import BaseModel


# Shared properties
class PurchaseBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    created: Optional[datetime] = None
    price: Optional[Decimal] = None
    value: Optional[Decimal] = None
    user_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    seller_id: Optional[UUID] = None


class PurchaseCreate(BaseModel):
    name: str
    created: datetime
    price: Decimal
    value: Decimal
    user_id: UUID
    seller_id: UUID
    category_id: Optional[UUID] = None


class PurchaseUpdate(PurchaseBase):
    id: UUID


# Properties shared by models stored in DB
class PurchaseInDBBase(PurchaseBase):
    id: UUID
    name: str
    created: datetime
    price: Decimal
    value: Decimal
    user_id: UUID
    seller_id: UUID
    category_id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Purchase(PurchaseInDBBase):
    pass


# Properties properties stored in DB
class PurchaseInDB(PurchaseInDBBase):
    pass
