import peewee as pw

from .main import MainModel

class Seller(MainModel):
    name = pw.CharField()
    user = pw.CharField()
