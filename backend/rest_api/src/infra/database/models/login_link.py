from uuid import uuid4

from sqlalchemy import UUID, Column, VARCHAR, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship

from .base import Model
from .user import User


class LoginLink(Model):
    """Model of temporary link of login through telegram"""
    __tablename__ = "login_link"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    link = Column(VARCHAR(255), nullable=False)
    created = Column(TIMESTAMP, nullable=False)
    user_id = Column(
        UUID,
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=True
    )
    user = relationship("User")

    def __repr__(self):
        return f"Unit {self.name} with id - <{self.id}>"
