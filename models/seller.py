import peewee as pw

from .main import MainModel

class Seller(MainModel):
    name = pw.CharField()
    user = pw.CharField()
    category = pw.ForeignKeyField(Category, backref='categories', null=True)
