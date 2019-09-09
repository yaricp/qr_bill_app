import peewee as pw
from .category import Category
from .seller import Seller
from .main import MainModel

class Purchase(MainModel):
    category = pw.ForeignKeyField(Category, backref='categories', null=True)
    name = pw.CharField()
    datetime = pw.DateTimeField()
    summ = pw.DecimalField()
    seller = pw.ForeignKeyField(Seller, backref='sellers', null=True)
    user = pw.CharField()
    pic = pw.CharField()
    confirm = pw.IntegerField(null=True)
