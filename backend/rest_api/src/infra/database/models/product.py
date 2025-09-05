from uuid import uuid4
from typing import Set
from sqlalchemy import UUID, Column, VARCHAR

from .base import Model


class Product(Model):
    """Model of product"""
    __tablename__ = "product"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    name = Column(VARCHAR(150), nullable=False, index=True)

    def __repr__(self):
        return f"Product {self.name} with id - <{self.id}>"
