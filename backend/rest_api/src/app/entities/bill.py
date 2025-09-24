from datetime import datetime
from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .goods import Goods
from .seller import Seller


# Shared properties
class BillBase(BaseModel):
    id: Optional[UUID] = None
    created: Optional[datetime] = None
    value: Optional[Decimal] = None
    image: Optional[str] = None
    payment_method: Optional[str] = None
    seller_id: Optional[UUID] = None
    user_id: Optional[UUID] = None


class BillCreate(BillBase):
    created: datetime
    value: Decimal
    seller_id: UUID
    user_id: UUID


# Properties to receive on item update
class BillUpdate(BillBase):
    id: UUID


# Properties shared by models stored in DB
class BillInDBBase(BillBase):
    id: UUID
    created: datetime
    value: Decimal
    seller_id: UUID
    seller: Seller
    goods_list: List[Goods] = []

    class Config:
        orm_mode = True


# Properties to return to client
class Bill(BillInDBBase):
    pass


# Properties properties stored in DB
class BillInDB(BillInDBBase):
    pass


class BillCreateByURL(BaseModel):
    link: str
    image: str
