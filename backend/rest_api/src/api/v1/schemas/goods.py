from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from .seller import Seller
from .unit import Unit
from .user_product import UserProduct


# Shared properties
class GoodsBase(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit_price_before_vat: Optional[Decimal] = None
    unit_price_after_vat: Optional[Decimal] = None
    rebate: Optional[Decimal] = Decimal(0.0)
    rebate_reducing: Optional[bool] = None
    price_before_vat: Optional[Decimal] = None
    vat_rate: Optional[Decimal] = None
    vat_amount: Optional[Decimal] = None
    price_after_vat: Optional[Decimal] = None
    unit_id: Optional[UUID] = None
    bill_id: Optional[UUID] = None


class GoodsCreate(BaseModel):
    name: str
    quantity: Decimal
    unit_price_before_vat: Decimal
    unit_price_after_vat: Decimal
    rebate: Decimal
    rebate_reducing: bool
    price_before_vat: Decimal
    vat_rate: Decimal
    vat_amount: Decimal
    price_after_vat: Decimal
    unit_id: UUID
    bill_id: UUID


class GoodsUpdate(GoodsBase):
    id: UUID


class GoodsForList(BaseModel):
    name: str


# Properties shared by models stored in DB
class GoodsInDBBase(GoodsBase):
    id: UUID
    name: str
    quantity: Decimal
    unit_price_before_vat: Decimal
    unit_price_after_vat: Decimal
    price_after_vat: Decimal
    seller: Seller
    unit: Unit
    bill_id: UUID
    user_product: Optional[UserProduct] = None

    class Config:
        orm_mode = True


# Properties to return to client
class Goods(GoodsInDBBase):
    pass


# Properties properties stored in DB
class GoodsInDB(GoodsInDBBase):
    pass


class GoodsCountByName(BaseModel):
    name: str
    count: Decimal


class GoodsSummByName(BaseModel):
    name: str
    summ: Decimal


class CategoryGoods(BaseModel):
    goods_id: UUID
    cat_id: UUID


class GoodsPrice(BaseModel):
    sum: Decimal
    created: datetime
