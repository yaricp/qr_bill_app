from hashlib import md5

from sqlalchemy import (
    INTEGER, Column, VARCHAR, ForeignKey, BOOLEAN
)
from sqlalchemy import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import Model
from .typesource import TypeSource


class Device(Model):
    """Model of device object in DB"""
    __tablename__ = 'devices'

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(150), nullable=True)
    type_source_id = Column(
        INTEGER,
        ForeignKey(TypeSource.id, ondelete="CASCADE")
    )
    type_source = relationship('TypeSource')
    serial_number = Column(VARCHAR(500), nullable=False, unique=True)
    
    note = Column(VARCHAR(1000), nullable=True)
    has_folder = Column(BOOLEAN, default=False)

    @hybrid_property
    def serial_number_hash(self):
        return md5(self.serial_number.encode()).hexdigest()

    @serial_number_hash.expression
    def serial_number_hash(cls):
        return func.hexdigest(func.md5(func.encode(cls.serial_number)))

    def __repr__(self):
        return f'Device {self.name} with id - <{self.id}>'