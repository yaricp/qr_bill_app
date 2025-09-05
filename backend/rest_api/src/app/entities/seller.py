from uuid import UUID
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel


# Shared properties
class SellerBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    official_name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    # phone: Optional[str] = None


class SellerCreate(SellerBase):
    official_name: str
    # address: str
    # city: str
    # phone: str


# Properties to receive on item update
class SellerUpdate(SellerBase):
    id: UUID


# Properties shared by models stored in DB
class SellerInDBBase(SellerBase):
    id: UUID
    name: str
    official_name: str
    # address: str
    # city: str

    class Config:
        orm_mode = True


# Properties to return to client
class Seller(SellerInDBBase):
    pass


# Properties properties stored in DB
class SellerInDB(SellerInDBBase):
    pass


class CountGoodsByNameSeller(BaseModel):
    name: str
    count: Decimal


class CountBillsByNameSeller(BaseModel):
    name: str
    count: int


class SummBillsByNameSeller(BaseModel):
    name: str
    summ: Decimal
