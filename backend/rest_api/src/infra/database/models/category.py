from typing import Set
from uuid import uuid4

from sqlalchemy import UUID, VARCHAR, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Model, association_goods_category, user_product_category
from .user import User


class Category(Model):
    """Model of category"""

    __tablename__ = "category"

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, nullable=False, unique=True, default=uuid4
    )
    name = Column(VARCHAR(150), nullable=True)
    user_id = Column(UUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=True)

    # goods: Mapped[Set["Goods"]] = relationship(
    #     secondary=association_goods_category,
    #     back_populates="categories"
    # )

    user_products: Mapped[Set["UserProduct"]] = relationship(
        secondary=user_product_category, back_populates="categories"
    )

    def __repr__(self):
        return f"Category {self.name} with id - <{self.id}>"
