from typing import Set
from uuid import uuid4

from sqlalchemy import UUID, VARCHAR, Column

from .base import Model


class Product(Model):
    """Model of product"""

    __tablename__ = "product"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    name = Column(VARCHAR(150), nullable=False, index=True)

    def __repr__(self):
        return f"Product {self.name} with id - <{self.id}>"
