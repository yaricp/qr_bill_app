from uuid import uuid4

from sqlalchemy import (
    UUID, Column, ForeignKey, Integer, BOOLEAN, VARCHAR, DECIMAL
)
# from sqlalchemy import func
from sqlalchemy.orm import relationship
# from sqlalchemy.ext.hybrid import hybrid_property

from .base import Model
from .category import Category
from .bill import Bill
from .unit import Unit
from .seller import Seller
# from .user import User


class Goods(Model):
    """Model of good item"""
    __tablename__ = "goods"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
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

    bill_id = Column(
        UUID,
        ForeignKey(Bill.id, ondelete="CASCADE"),
        nullable=False
    )
    bill = relationship("Bill")

    seller_id = Column(
        UUID,
        ForeignKey(Seller.id, ondelete="CASCADE"),
        nullable=True
    )
    seller = relationship("Seller")

    category_id = Column(
        UUID,
        ForeignKey(Category.id, ondelete="CASCADE"),
        nullable=True
    )
    category = relationship("Category")

    def __repr__(self):
        return f"Goods {self.name} with id - <{self.id}>"
