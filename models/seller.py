import peewee as pw
from playhouse.sqlite_ext import *

from .main import MainModel
from .category import Category

class Seller(MainModel):
    name = pw.CharField()
    user = pw.CharField()
    category = pw.ForeignKeyField(Category, backref='categories', null=True)
    longitude = pw.FloatField() #83.256584
    latitude = pw.FloatField()  #54.838643
