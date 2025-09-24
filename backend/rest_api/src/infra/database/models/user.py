from hashlib import sha256
from uuid import uuid4

from sqlalchemy import INTEGER, UUID, VARCHAR, Boolean, Column
from sqlalchemy.orm import relationship

from .base import Model


class User(Model):
    """Model of user object in DB"""

    __tablename__ = "users"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    is_admin = Column(Boolean, default=False)
    email = Column(VARCHAR(150), nullable=True)
    email_verified = Column(Boolean, default=False)
    phone = Column(VARCHAR(14), nullable=True)
    phone_verified = Column(Boolean, default=False)
    login = Column(VARCHAR(150), nullable=True)
    tg_name = Column(VARCHAR(150), nullable=True)
    tg_id = Column(INTEGER)
    tg_verified = Column(Boolean, default=False)
    password_hash = Column(VARCHAR(4000), nullable=True)
    password_salt = Column(VARCHAR(24), nullable=True)
    lang = Column(VARCHAR(4), nullable=False, default="ru")

    links = relationship("LoginLink")

    def set_password_hash(self, password: str) -> bool:
        self.password_hash = sha256(password.encode()).hexdigest()
        if self.password_hash:
            return False
        return True

    def __repr__(self):
        return f"User {self.id}"
