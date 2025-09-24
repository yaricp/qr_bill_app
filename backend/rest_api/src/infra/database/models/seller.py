from uuid import uuid4

from sqlalchemy import UUID, VARCHAR, Column
# from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import relationship

from .base import Model


class Seller(Model):
    """Model of seller"""

    __tablename__ = "seller"

    id = Column(UUID, primary_key=True, nullable=False, unique=True, default=uuid4)
    name = Column(VARCHAR(50), nullable=False)
    official_name = Column(VARCHAR(250), nullable=False)
    address = Column(VARCHAR(150), nullable=True)
    city = Column(VARCHAR(50), nullable=True)
    bills_list = relationship("Bill")
    goods_list = relationship("Goods")
    # position = Column(
    #     Geometry(geometry_type="POINT", srid=4326),
    #     nullable=True
    # )
    # , spatial_index=True

    def __repr__(self):
        return f"Seller {self.name} with id - <{self.id}>"
