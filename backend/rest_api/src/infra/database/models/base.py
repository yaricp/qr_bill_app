from uuid import uuid4
from sqlalchemy import UUID, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

from .. import db_session


Model = declarative_base()
Model.query = db_session.query_property()

association_goods_category = Table(
    "association_goods_category",
    Model.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("goods_id", ForeignKey("goods.id")),
    Column("cat_id", ForeignKey("category.id"))
)

user_product_category = Table(
    "user_product_category",
    Model.metadata,
    Column(
        "id", UUID, primary_key=True, nullable=False,
        unique=True, default=uuid4
    ),
    Column("user_product_id", ForeignKey("user_product.id")),
    Column("cat_id", ForeignKey("category.id"))
)
