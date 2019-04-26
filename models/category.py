import peewee as pw

from .main import MainModel

class Category(MainModel):
    
    name = pw.CharField()
    user = pw.CharField()
    
    
