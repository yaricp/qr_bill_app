from uuid import uuid4
from typing import Set
from sqlalchemy import UUID, Column, VARCHAR

from sqlalchemy.orm import relationship, Mapped

from .base import Model, association_product_category


class Product(Model):
    """Model of product"""
    __tablename__ = "product"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    name = Column(VARCHAR(150), nullable=False, index=True)

    categories: Mapped[Set["Category"]] = relationship(
        secondary=association_product_category,
        back_populates="products"
    )

    def __repr__(self):
        return f"Product {self.name} with id - <{self.id}>"
