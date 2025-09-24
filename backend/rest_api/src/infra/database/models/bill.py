from uuid import uuid4

from sqlalchemy import DECIMAL, TIMESTAMP, UUID, VARCHAR, Column, ForeignKey
# from sqlalchemy import func
from sqlalchemy.orm import relationship

from .base import Model
# from .category import Category
from .seller import Seller
from .user import User

# from sqlalchemy.ext.hybrid import hybrid_property


class Bill(Model):
    """Model of Bill"""

    __tablename__ = "bill"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    created = Column(TIMESTAMP, nullable=False)
    value = Column(DECIMAL(6, 2), nullable=False)
    payment_method = Column(VARCHAR(50), nullable=True)
    image = Column(VARCHAR(100000), nullable=True)

    seller_id = Column(UUID, ForeignKey(Seller.id, ondelete="CASCADE"), nullable=False)
    seller = relationship("Seller")

    user_id = Column(UUID, ForeignKey(User.id, ondelete="CASCADE"), nullable=True)
    user = relationship("User")

    goods_list = relationship("Goods")

    def __repr__(self):
        return f"Bill {self.created} - {self.value} with id - <{self.id}>"
