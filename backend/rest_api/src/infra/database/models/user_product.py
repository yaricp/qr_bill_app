from uuid import uuid4
from typing import Set
from sqlalchemy import UUID, Column, ForeignKey

from sqlalchemy.orm import relationship, Mapped

from .base import Model, user_product_category
from .product import Product
from .user import User


class UserProduct(Model):
    """Model of user product"""
    __tablename__ = "user_product"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    user_id = Column(
        UUID,
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=True
    )
    product_id = Column(
        UUID, ForeignKey(Product.id), nullable=True
    )
    product = relationship("Product")

    categories: Mapped[Set["Category"]] = relationship(
        secondary=user_product_category,
        back_populates="user_products"
    )

    def __repr__(self):
        return f"UserProduct {self.product.name} with id - <{self.id}>"\
            f" for user with {self.user_id}"
