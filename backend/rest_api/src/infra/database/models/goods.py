from uuid import uuid4
from typing import Set
from sqlalchemy import (
    UUID, Column, ForeignKey, Integer, BIGINT, BOOLEAN,
    VARCHAR, DECIMAL
)

from sqlalchemy.orm import relationship, Mapped

from .base import Model, association_goods_category
from .bill import Bill
from .unit import Unit
from .seller import Seller
from .user import User
from .user_product import UserProduct


class Goods(Model):
    """Model of good item"""
    __tablename__ = "goods"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    fiscal_id = Column(BIGINT, nullable=True)
    name = Column(VARCHAR(150), nullable=False)
    quantity = Column(DECIMAL(6, 4), nullable=False)
    unit_price_before_vat = Column(DECIMAL(6, 4), nullable=False)
    unit_price_after_vat = Column(DECIMAL(6, 4), nullable=False)
    rebate = Column(DECIMAL(6, 4), nullable=False)
    rebate_reducing = Column(BOOLEAN, default=False)
    price_before_vat = Column(DECIMAL(6, 4), nullable=False)
    vat_rate = Column(Integer, nullable=False)
    vat_amount = Column(DECIMAL(6, 4), nullable=False)
    price_after_vat = Column(DECIMAL(6, 4), nullable=False)

    unit_id = Column(
        UUID, ForeignKey(Unit.id), nullable=False
    )
    unit = relationship("Unit")

    user_product_id = Column(
        UUID, ForeignKey(UserProduct.id), nullable=True
    )
    user_product = relationship("UserProduct")

    bill_id = Column(
        UUID,
        ForeignKey(Bill.id, ondelete="CASCADE"),
        nullable=False
    )
    bill = relationship("Bill")

    user_id = Column(
        UUID,
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=True
    )
    user = relationship("User")

    seller_id = Column(
        UUID,
        ForeignKey(Seller.id, ondelete="CASCADE"),
        nullable=True
    )
    seller = relationship("Seller")

    categories: Mapped[Set["Category"]] = relationship(
        secondary=association_goods_category,
        back_populates="goods"
    )

    def __repr__(self):
        return f"Goods {self.name} with id - <{self.id}>"
