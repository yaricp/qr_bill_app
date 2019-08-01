import peewee as pw
from playhouse.sqlite_ext import *

from .main import MainModel
from .category import Category

class Seller(MainModel):
    name = pw.CharField()
    user = pw.CharField()
    category = pw.ForeignKeyField(Category, backref='categories', null=True)
    longitude = pw.FloatField(null=True) #83.256584
    latitude = pw.FloatField(null=True)  #54.838643
