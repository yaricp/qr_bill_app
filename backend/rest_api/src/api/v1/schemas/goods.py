from uuid import UUID
from datetime import datetime
from decimal import Decimal

from typing import Optional

from pydantic import BaseModel


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
    category_id: Optional[UUID] = None


    {
        'id': 4598966187,
        'name': 'Kroasan ljesnik 90g  ',
        'code': '2000004068257',
        'unit': 'KOM',
        'quantity': 1.0,
        'unitPriceBeforeVat': 0.9511,
        'unitPriceAfterVat': 0.85,
        'rebate': 26.14,
        'rebateReducing': False,
        'priceBeforeVat': 0.7025,
        'vatRate': 21,
        'vatAmount': 0.1475,
        'priceAfterVat': 0.85,
        'exemptFromVat': None,
        'voucherSold': None,
        'vd': None,
        'vsn': None,
        'investment': False
    }


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
    price_after_vat:  Decimal
    unit_id: UUID
    bill_id: UUID


class GoodsUpdate(GoodsBase):
    id: UUID


# Properties shared by models stored in DB
class GoodsInDBBase(GoodsBase):
    id: UUID
    name: str
    quantity: Decimal
    unit_price_before_vat: Decimal
    unit_price_after_vat: Decimal
    rebate: Decimal
    rebate_reducing: bool
    price_before_vat: Decimal
    vat_rate: Decimal
    vat_amount: Decimal
    price_after_vat:  Decimal
    unit_id: UUID
    bill_id: UUID

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
