from uuid import uuid4

from sqlalchemy import UUID, VARCHAR, Column

from .base import Model


class Unit(Model):
    """Model of category"""

    __tablename__ = "unit"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    name = Column(VARCHAR(150), nullable=True)
    # has_folder = Column(BOOLEAN, default=False)

    def __repr__(self):
        return f"Unit {self.name} with id - <{self.id}>"
