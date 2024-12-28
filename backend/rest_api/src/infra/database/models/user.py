from uuid import uuid4
from hashlib import sha256

from sqlalchemy import INTEGER, Column, VARCHAR, UUID

from .base import Model


class User(Model):
    """Model of user object in DB"""
    __tablename__ = "users"

    id = Column(
        UUID, primary_key=True, nullable=False, unique=True,
        default=uuid4
    )
    email = Column(VARCHAR(200), nullable=True)
    login = Column(VARCHAR(150), nullable=True)
    tg_name = Column(VARCHAR(150), nullable=True)
    tg_id = Column(INTEGER)
    password_hash = Column(VARCHAR(4000), nullable=False)

    def set_password_hash(self, password: str) -> bool:
        self.password_hash = sha256(password.encode()).hexdigest()
        if self.password_hash:
            return False
        return True

    def __repr__(self):
        return f"User {self.id}"