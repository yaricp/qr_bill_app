from uuid import uuid4

from sqlalchemy import (
    UUID, INTEGER, Column, VARCHAR, ForeignKey, DATETIME, DECIMAL
)
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Model
from .category import Category
from .seller import Seller
from .user import User


class Purchase(Model):
    """Model of Purchase"""
    __tablename__ = "purchase"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    datetime = Column(DATETIME, nullable=False)
    name = Column(VARCHAR(150), nullable=False)
    price = Column(DECIMAL, nullable=False)
    value = Column(DECIMAL, nullable=False)

    user_id = Column(
        UUID, ForeignKey(User.id, ondelete="CASCADE")
    )
    user = relationship("User")

    category_id = Column(
        UUID, ForeignKey(Category.id, ondelete="CASCADE")
    )
    category = relationship("Category")

    seller_id = Column(
        UUID, ForeignKey(Seller.id, ondelete="CASCADE")
    )
    seller = relationship("Seller")

    def __repr__(self):
        return f"Purchase {self.name} with id - <{self.id}>"
