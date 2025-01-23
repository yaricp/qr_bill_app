from uuid import uuid4
from typing import Set
from sqlalchemy.orm import (
    relationship, Mapped, mapped_column
)
from sqlalchemy import (
    UUID, Column, VARCHAR, ForeignKey
)

from .base import (
    Model, association_goods_category, association_product_category
)
from .user import User
from .goods import Goods
from .product import Product


class Category(Model):
    """Model of category"""
    __tablename__ = "category"

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    name = Column(VARCHAR(150), nullable=True)
    user_id = Column(
        UUID,
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=True
    )

    # goods: Mapped[Set[Goods]] = relationship(
    #     secondary=association_goods_category,
    #     back_populates="categories"
    # )

    products: Mapped[Set[Product]] = relationship(
        secondary=association_product_category,
        back_populates="categories"
    )

    def __repr__(self):
        return f"Category {self.name} with id - <{self.id}>"
