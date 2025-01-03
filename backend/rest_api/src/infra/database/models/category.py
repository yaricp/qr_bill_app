from uuid import uuid4

from sqlalchemy.orm import relationship
from sqlalchemy import UUID, Column, VARCHAR, ForeignKey

from .base import Model
from .user import User


class Category(Model):
    """Model of category"""
    __tablename__ = "category"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    name = Column(VARCHAR(150), nullable=True)
    # has_folder = Column(BOOLEAN, default=False)
    user_id = Column(
        UUID,
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=True
    )
    user = relationship("User")

    def __repr__(self):
        return f"Category {self.name} with id - <{self.id}>"
