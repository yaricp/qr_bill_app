from uuid import uuid4
from typing import List, Set
from sqlalchemy.orm import (
    relationship, Mapped, DeclarativeBase, mapped_column
)
from sqlalchemy import (
    Table, UUID, Column, VARCHAR, ForeignKey
)

from .base import Model, association_goods_category
from .user import User
from .goods import Goods


class Category(Model):
    """Model of category"""
    __tablename__ = "category"

    # id = Column(
    #     UUID, primary_key=True
    # )

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

    goods: Mapped[Set[Goods]] = relationship(
        secondary=association_goods_category,
        back_populates="categories"
    )

    def __repr__(self):
        return f"Category {self.name} with id - <{self.id}>"
